"""
End-to-End tests that validate AI-generated script quality.

This tests the QUALITY of AI output by:
1. Using mock project documentation (not this project's docs)
2. Having pre-written "golden" scripts that are known to be correct
3. Asking AI to generate scripts from mock docs
4. Asking AI to compare generated vs golden scripts
5. Validating that generated scripts don't miss critical steps
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, Mock
from doctai.orchestrator import DocumentationTester
from doctai.ai_client import AIClient
from doctai.config import ConfigLoader


class TestAIScriptQuality:
    """Test that AI generates high-quality, complete scripts."""
    
    @pytest.fixture
    def mock_projects_dir(self):
        """Get the mock projects directory."""
        return Path(__file__).parent.parent / "fixtures" / "mock-projects"
    
    def _read_golden_script(self, project_dir):
        """Read the golden (correct) script for a project."""
        golden_path = project_dir / "golden_script.sh"
        if not golden_path.exists():
            pytest.skip(f"Golden script not found: {golden_path}")
        return golden_path.read_text()
    
    def _extract_generated_script(self, results):
        """Extract the generated script from test results."""
        if 'scripts' not in results or not results['scripts']:
            return None
        
        # Combine all generated scripts
        generated = []
        for script_name, script_info in results['scripts'].items():
            if 'content' in script_info:
                generated.append(script_info['content'])
        
        return '\n\n'.join(generated) if generated else None
    
    def _load_config_for_test(self):
        """Load configuration from .doctai.yml file (same as CLI behavior)."""
        config_loader = ConfigLoader()
        config_loader.load()
        return config_loader
    
    def _ask_ai_to_compare(self, ai_client, generated_script, golden_script, doc_name):
        """
        Ask AI to compare generated script with golden script.
        
        Returns: (is_adequate: bool, explanation: str)
        """
        comparison_prompt = f"""You are a code review expert. I have two scripts:

1. GOLDEN SCRIPT (known to be correct):
```bash
{golden_script}
```

2. GENERATED SCRIPT (from AI analyzing documentation):
```bash
{generated_script}
```

Compare these scripts and determine if the GENERATED script is adequate.

The GENERATED script is adequate if it:
- Covers all critical installation steps from the GOLDEN script
- Doesn't skip any essential dependencies
- Tests/verifies the functionality properly
- Has proper error handling (if golden script has it)

The GENERATED script can:
- Have different formatting or style
- Use different approaches (as long as they work)
- Have additional helpful steps
- Be more verbose or concise

Respond in this EXACT format:
ADEQUATE: YES or NO
REASON: <one-line explanation>
MISSING: <comma-separated list of critical missing steps, or "none">

Example responses:
ADEQUATE: YES
REASON: Generated script covers all essential steps with proper verification
MISSING: none

ADEQUATE: NO
REASON: Generated script missing dependency installation and verification steps
MISSING: pip install flask flask-cors, API endpoint testing
"""
        
        try:
            response = ai_client.send_message(comparison_prompt)
            
            # Parse response
            lines = response.strip().split('\n')
            adequate = None
            reason = ""
            missing = []
            
            for line in lines:
                if line.startswith('ADEQUATE:'):
                    adequate = 'YES' in line.upper()
                elif line.startswith('REASON:'):
                    reason = line.replace('REASON:', '').strip()
                elif line.startswith('MISSING:'):
                    missing_str = line.replace('MISSING:', '').strip()
                    if missing_str.lower() != 'none':
                        missing = [m.strip() for m in missing_str.split(',')]
            
            return adequate, reason, missing
        
        except Exception as e:
            pytest.fail(f"Failed to compare scripts with AI: {e}")
    
    @pytest.mark.e2e
    @pytest.mark.requires_api
    @pytest.mark.skipif(
        "DOCTAI_API_KEY" not in os.environ,
        reason="Requires DOCTAI_API_KEY environment variable"
    )
    def test_flask_api_script_quality(self, mock_projects_dir):
        """Test that AI generates adequate script for Flask API documentation."""
        project_dir = mock_projects_dir / "flask-api"
        readme_path = project_dir / "README.md"
        
        if not readme_path.exists():
            pytest.skip(f"Mock project not found: {readme_path}")
        
        # Step 1: Read golden script
        golden_script = self._read_golden_script(project_dir)
        
        # Step 2: Load config from .doctai.yml (same as CLI behavior)
        config_loader = self._load_config_for_test()
        provider = config_loader.get_provider() or 'anthropic'
        model = config_loader.get_model() or 'claude-sonnet-4-20250514'
        
        # Step 3: Create AI client with config values
        from doctai.ai_client import AIClient
        ai_client = AIClient(
            api_key=os.environ['DOCTAI_API_KEY'],
            provider=provider,
            model=model
        )
        
        # Step 4: Use doctai to generate script from README
        tester = DocumentationTester(
            ai_client=ai_client,
            verbose=True
        )
        
        results = tester.test_documentation([str(readme_path)])
        
        # Check for errors in results
        if 'error' in results:
            pytest.fail(f"Documentation testing failed: {results['error']}")
        
        generated_script = self._extract_generated_script(results)
        if generated_script is None:
            pytest.fail(f"No script was generated. Results: {results}")
        
        # Step 4: Ask AI to compare scripts (reuse the same client)
        
        is_adequate, reason, missing = self._ask_ai_to_compare(
            ai_client, generated_script, golden_script, "Flask API"
        )
        
        # Step 4: Assert quality
        print(f"\n{'='*60}")
        print(f"Flask API Script Quality Check")
        print(f"{'='*60}")
        print(f"Adequate: {is_adequate}")
        print(f"Reason: {reason}")
        if missing:
            print(f"Missing steps: {', '.join(missing)}")
        print(f"{'='*60}\n")
        
        assert is_adequate, f"Generated script is inadequate: {reason}. Missing: {', '.join(missing)}"
    
    @pytest.mark.e2e
    @pytest.mark.requires_api
    @pytest.mark.skipif(
        "DOCTAI_API_KEY" not in os.environ,
        reason="Requires DOCTAI_API_KEY environment variable"
    )
    def test_nodejs_cli_script_quality(self, mock_projects_dir):
        """Test that AI generates adequate script for Node.js CLI documentation."""
        project_dir = mock_projects_dir / "nodejs-cli"
        readme_path = project_dir / "README.md"
        
        if not readme_path.exists():
            pytest.skip(f"Mock project not found: {readme_path}")
        
        golden_script = self._read_golden_script(project_dir)
        
        # Load config from .doctai.yml (same as CLI behavior)
        config_loader = self._load_config_for_test()
        provider = config_loader.get_provider() or 'anthropic'
        model = config_loader.get_model() or 'claude-sonnet-4-20250514'
        
        # Create AI client with config values
        from doctai.ai_client import AIClient
        ai_client = AIClient(
            api_key=os.environ['DOCTAI_API_KEY'],
            provider=provider,
            model=model
        )
        
        tester = DocumentationTester(
            ai_client=ai_client,
            verbose=True
        )
        
        results = tester.test_documentation([str(readme_path)])
        
        # Check for errors in results
        if 'error' in results:
            pytest.fail(f"Documentation testing failed: {results['error']}")
        
        generated_script = self._extract_generated_script(results)
        if generated_script is None:
            pytest.fail(f"No script was generated. Results: {results}")
        
        is_adequate, reason, missing = self._ask_ai_to_compare(
            ai_client, generated_script, golden_script, "Node.js CLI"
        )
        
        print(f"\n{'='*60}")
        print(f"Node.js CLI Script Quality Check")
        print(f"{'='*60}")
        print(f"Adequate: {is_adequate}")
        print(f"Reason: {reason}")
        if missing:
            print(f"Missing steps: {', '.join(missing)}")
        print(f"{'='*60}\n")
        
        assert is_adequate, f"Generated script is inadequate: {reason}. Missing: {', '.join(missing)}"
    
    @pytest.mark.e2e
    @pytest.mark.requires_api
    @pytest.mark.skipif(
        "DOCTAI_API_KEY" not in os.environ,
        reason="Requires DOCTAI_API_KEY environment variable"
    )
    def test_python_data_analysis_script_quality(self, mock_projects_dir):
        """Test that AI generates adequate script for Python data analysis documentation."""
        project_dir = mock_projects_dir / "python-data-analysis"
        readme_path = project_dir / "README.md"
        
        if not readme_path.exists():
            pytest.skip(f"Mock project not found: {readme_path}")
        
        golden_script = self._read_golden_script(project_dir)
        
        # Load config from .doctai.yml (same as CLI behavior)
        config_loader = self._load_config_for_test()
        provider = config_loader.get_provider() or 'anthropic'
        model = config_loader.get_model() or 'claude-sonnet-4-20250514'
        
        # Create AI client with config values
        from doctai.ai_client import AIClient
        ai_client = AIClient(
            api_key=os.environ['DOCTAI_API_KEY'],
            provider=provider,
            model=model
        )
        
        tester = DocumentationTester(
            ai_client=ai_client,
            verbose=True
        )
        
        results = tester.test_documentation([str(readme_path)])
        
        # Check for errors in results
        if 'error' in results:
            pytest.fail(f"Documentation testing failed: {results['error']}")
        
        generated_script = self._extract_generated_script(results)
        if generated_script is None:
            pytest.fail(f"No script was generated. Results: {results}")
        
        is_adequate, reason, missing = self._ask_ai_to_compare(
            ai_client, generated_script, golden_script, "Python Data Analysis"
        )
        
        print(f"\n{'='*60}")
        print(f"Python Data Analysis Script Quality Check")
        print(f"{'='*60}")
        print(f"Adequate: {is_adequate}")
        print(f"Reason: {reason}")
        if missing:
            print(f"Missing steps: {', '.join(missing)}")
        print(f"{'='*60}\n")
        
        assert is_adequate, f"Generated script is inadequate: {reason}. Missing: {', '.join(missing)}"
    
    @pytest.mark.unit
    def test_mock_projects_exist(self, mock_projects_dir):
        """Verify that mock projects and golden scripts are set up correctly."""
        projects = ['flask-api', 'nodejs-cli', 'python-data-analysis']
        
        for project in projects:
            project_dir = mock_projects_dir / project
            assert project_dir.exists(), f"Mock project missing: {project}"
            
            readme = project_dir / "README.md"
            assert readme.exists(), f"README missing for {project}"
            
            golden = project_dir / "golden_script.sh"
            assert golden.exists(), f"Golden script missing for {project}"
            
            # Verify golden script is executable
            assert os.access(golden, os.X_OK), f"Golden script not executable: {project}"
    
    @pytest.mark.unit
    def test_golden_scripts_are_valid(self, mock_projects_dir):
        """Verify that golden scripts have proper structure."""
        projects = ['flask-api', 'nodejs-cli', 'python-data-analysis']
        
        for project in projects:
            golden_path = mock_projects_dir / project / "golden_script.sh"
            content = golden_path.read_text()
            
            # Basic validation
            assert '#!/bin/bash' in content, f"Golden script missing shebang: {project}"
            assert 'set -e' in content, f"Golden script missing 'set -e': {project}"
            assert 'echo' in content, f"Golden script has no output: {project}"
            
            # Should have installation steps
            assert 'install' in content.lower(), f"Golden script missing install steps: {project}"
            
            # Should have verification/testing
            assert any(word in content.lower() for word in ['test', 'verify', 'check']), \
                f"Golden script missing verification: {project}"


class TestAIComparisonLogic:
    """Test the AI comparison logic itself (with mocked responses)."""
    
    @pytest.mark.unit
    def test_parse_adequate_response(self):
        """Test parsing of AI comparison response."""
        response = """ADEQUATE: YES
REASON: Generated script covers all essential steps
MISSING: none"""
        
        # Simulate parsing
        lines = response.strip().split('\n')
        adequate = None
        reason = ""
        missing = []
        
        for line in lines:
            if line.startswith('ADEQUATE:'):
                adequate = 'YES' in line.upper()
            elif line.startswith('REASON:'):
                reason = line.replace('REASON:', '').strip()
            elif line.startswith('MISSING:'):
                missing_str = line.replace('MISSING:', '').strip()
                if missing_str.lower() != 'none':
                    missing = [m.strip() for m in missing_str.split(',')]
        
        assert adequate is True
        assert "essential steps" in reason
        assert len(missing) == 0
    
    @pytest.mark.unit
    def test_parse_inadequate_response(self):
        """Test parsing of inadequate script response."""
        response = """ADEQUATE: NO
REASON: Missing dependency installation and verification
MISSING: pip install flask, API testing, error handling"""
        
        lines = response.strip().split('\n')
        adequate = None
        missing = []
        
        for line in lines:
            if line.startswith('ADEQUATE:'):
                adequate = 'YES' in line.upper()
            elif line.startswith('MISSING:'):
                missing_str = line.replace('MISSING:', '').strip()
                if missing_str.lower() != 'none':
                    missing = [m.strip() for m in missing_str.split(',')]
        
        assert adequate is False
        assert len(missing) == 3
        assert 'pip install flask' in missing

