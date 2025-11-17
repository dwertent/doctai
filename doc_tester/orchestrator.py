"""
Main orchestrator module.

Manages the entire documentation testing workflow:
1. Fetch documentation
2. Communicate with AI to generate test scripts
3. Execute generated scripts
4. Report results
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from doc_tester.fetcher import DocumentationFetcher
from doc_tester.ai_client import AIClient
from doc_tester.executor import ScriptExecutor


class DocumentationTester:
    """Main orchestrator for documentation testing."""
    
    SYSTEM_PROMPT = """You are an expert software engineer and documentation tester. Your job is to:

1. Analyze provided documentation (setup guides, installation instructions, tutorials, etc.)
2. Generate executable test scripts (bash, python, or other languages) that follow the documentation
3. The scripts should install prerequisites, set up the environment, and run examples/tests as described
4. Make scripts idempotent and safe to run multiple times when possible
5. Include error handling and informative output
6. Use appropriate tools and package managers (apt, brew, pip, npm, etc.)
7. Consider the operating system and environment

When I provide documentation, you should:
- Understand what needs to be installed/configured
- Generate ONE OR MORE complete, executable scripts
- Format each script clearly with markers like:
  ```bash
  #!/bin/bash
  # Script content here
  ```
  or
  ```python
  # Python script content here
  ```
- Explain what each script does
- List any assumptions or requirements

Be practical and focus on making the documentation work. If something is ambiguous, make reasonable assumptions."""

    def __init__(
        self,
        ai_client: AIClient,
        work_dir: Optional[str] = None,
        verbose: bool = True
    ):
        """
        Initialize documentation tester.
        
        Args:
            ai_client: Configured AI client
            work_dir: Working directory for test execution
            verbose: Whether to print detailed output
        """
        self.ai_client = ai_client
        self.work_dir = work_dir
        self.verbose = verbose
        self.fetcher = DocumentationFetcher()
    
    def test_documentation(
        self,
        sources: List[str],
        max_iterations: int = 3,
        stop_on_failure: bool = False,
        custom_instructions: Optional[str] = None
    ) -> Dict:
        """
        Test documentation from given sources.
        
        Args:
            sources: List of documentation sources (paths or URLs)
            max_iterations: Maximum number of AI conversation iterations
            stop_on_failure: Whether to stop if a script fails
            custom_instructions: Optional additional instructions for the AI
            
        Returns:
            Dictionary with test results
        """
        results = {
            "success": False,
            "documentation_sources": sources,
            "documentation_count": 0,
            "scripts_generated": 0,
            "scripts_executed": 0,
            "scripts_passed": 0,
            "scripts_failed": 0,
            "scripts": {},  # Store generated scripts here
            "details": []
        }
        
        # Step 1: Fetch documentation
        if self.verbose:
            print("\n" + "="*80)
            print("STEP 1: Fetching Documentation")
            print("="*80 + "\n")
        
        try:
            docs = self.fetcher.fetch_multiple(sources)
            results["documentation_count"] = len(docs)
            
            if self.verbose:
                for source, content in docs.items():
                    print(f"✓ Fetched: {source} ({len(content)} characters)")
        except Exception as e:
            results["error"] = f"Failed to fetch documentation: {str(e)}"
            return results
        
        # Step 2: Send documentation to AI and get test scripts
        if self.verbose:
            print("\n" + "="*80)
            print("STEP 2: Analyzing Documentation with AI")
            print("="*80 + "\n")
        
        try:
            scripts = self._generate_test_scripts(docs, max_iterations, custom_instructions)
            results["scripts_generated"] = len(scripts)
            results["scripts"] = scripts  # Store generated scripts in results
            
            if self.verbose:
                print(f"\n✓ Generated {len(scripts)} test script(s)")
        except Exception as e:
            results["error"] = f"Failed to generate test scripts: {str(e)}"
            return results
        
        if not scripts:
            results["error"] = "No test scripts were generated"
            return results
        
        # Step 3: Execute test scripts
        if self.verbose:
            print("\n" + "="*80)
            print("STEP 3: Executing Test Scripts")
            print("="*80 + "\n")
        
        try:
            # Use first documentation source as context for naming
            source_context = sources[0] if sources else None
            
            with ScriptExecutor(
                work_dir=self.work_dir, 
                verbose=self.verbose,
                source_context=source_context,
                save_generated_scripts=True
            ) as executor:
                execution_results = executor.execute_multiple_scripts(
                    scripts,
                    stop_on_failure=stop_on_failure
                )
                
                results["scripts_executed"] = len(execution_results)
                
                for script_name, (success, stdout, stderr) in execution_results.items():
                    if success:
                        results["scripts_passed"] += 1
                    else:
                        results["scripts_failed"] += 1
                    
                    results["details"].append({
                        "script": script_name,
                        "success": success,
                        "stdout": stdout[:1000],  # Limit output size
                        "stderr": stderr[:1000]
                    })
        
        except Exception as e:
            results["error"] = f"Failed to execute scripts: {str(e)}"
            return results
        
        # Determine overall success
        results["success"] = (
            results["scripts_executed"] > 0 and
            results["scripts_failed"] == 0
        )
        
        # Step 4: Print summary
        if self.verbose:
            self._print_summary(results)
        
        return results
    
    def _generate_test_scripts(
        self,
        docs: Dict[str, str],
        max_iterations: int,
        custom_instructions: Optional[str] = None
    ) -> Dict[str, Dict[str, str]]:
        """
        Generate test scripts by communicating with AI.
        
        Args:
            docs: Dictionary of documentation content
            max_iterations: Maximum conversation iterations
            custom_instructions: Optional additional instructions for the AI
            
        Returns:
            Dictionary of scripts with their content and type
        """
        # Prepare documentation for AI
        doc_text = self._format_docs_for_ai(docs)
        
        # Build initial prompt
        prompt_parts = [f"Here is the documentation I need you to test:\n\n{doc_text}\n"]
        
        # Add custom instructions if provided
        if custom_instructions:
            prompt_parts.append(f"\n## Additional Instructions\n\n{custom_instructions}\n")
        
        prompt_parts.append("""
Please analyze this documentation and generate executable test scripts that:
1. Install any required prerequisites
2. Follow the setup/installation instructions
3. Run any examples or tests mentioned
4. Verify everything works as documented""")
        
        if custom_instructions:
            prompt_parts.append("\n5. Address the additional instructions provided above")
        
        prompt_parts.append("""

Generate complete, ready-to-run scripts. Use bash scripts for system setup/installation and Python scripts if needed for application testing.

Format each script clearly with code blocks like:
```bash
#!/bin/bash
# your script here
```

or

```python
# your Python script here
```
""")
        
        initial_prompt = ''.join(prompt_parts)
        
        # Get AI response
        ai_response = self.ai_client.send_message(initial_prompt, self.SYSTEM_PROMPT)
        
        # Extract scripts from AI response
        scripts = self._extract_scripts_from_response(ai_response)
        
        # Could implement iteration here if needed to refine scripts
        # For now, return the first set of generated scripts
        
        return scripts
    
    def _format_docs_for_ai(self, docs: Dict[str, str]) -> str:
        """Format documentation for AI consumption."""
        formatted = []
        
        for source, content in docs.items():
            formatted.append(f"=== Documentation from: {source} ===\n")
            formatted.append(content)
            formatted.append("\n" + "="*80 + "\n")
        
        return "\n".join(formatted)
    
    def _extract_scripts_from_response(
        self,
        response: str
    ) -> Dict[str, Dict[str, str]]:
        """
        Extract code blocks from AI response.
        
        Args:
            response: AI response text
            
        Returns:
            Dictionary of scripts with metadata
        """
        scripts = {}
        
        # Pattern to match code blocks with language identifier
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        
        for i, (language, content) in enumerate(matches, 1):
            # Determine script type
            script_type = language.lower()
            
            # Skip non-executable languages
            if script_type in ['json', 'yaml', 'yml', 'toml', 'xml', 'html', 'css', 'markdown', 'md', 'txt']:
                continue
            
            # Normalize script types
            if script_type in ['sh', 'shell', 'bash']:
                script_type = 'bash'
            elif script_type in ['py', 'python3']:
                script_type = 'python'
            
            script_name = f"script_{i}_{script_type}"
            
            scripts[script_name] = {
                'content': content.strip(),
                'type': script_type
            }
        
        return scripts
    
    def _print_summary(self, results: Dict):
        """Print test results summary."""
        print("\n" + "="*80)
        print("TEST RESULTS SUMMARY")
        print("="*80 + "\n")
        
        print(f"Documentation sources: {results['documentation_count']}")
        print(f"Scripts generated: {results['scripts_generated']}")
        print(f"Scripts executed: {results['scripts_executed']}")
        print(f"Scripts passed: {results['scripts_passed']} ✓")
        print(f"Scripts failed: {results['scripts_failed']} ✗")
        
        if results.get("error"):
            print(f"\nError: {results['error']}")
        
        print(f"\nOverall result: {'✓ SUCCESS' if results['success'] else '✗ FAILURE'}")
        print("="*80 + "\n")

