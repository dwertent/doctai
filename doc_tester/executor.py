"""
Script executor module.

Handles safe execution of generated test scripts.
"""

import os
import subprocess
import tempfile
import shutil
import random
import string
from typing import Dict, Optional, Tuple
from pathlib import Path
import re


class ScriptExecutor:
    """Executes generated test scripts safely."""
    
    def __init__(
        self, 
        work_dir: Optional[str] = None, 
        verbose: bool = True,
        source_context: Optional[str] = None,
        save_generated_scripts: bool = True
    ):
        """
        Initialize script executor.
        
        Args:
            work_dir: Working directory for script execution (creates temp if not provided)
            verbose: Whether to print detailed output
            source_context: Source path/URL for naming generated scripts
            save_generated_scripts: Whether to save generated scripts with _gen- prefix
        """
        self.verbose = verbose
        self.source_context = source_context
        self.save_generated_scripts = save_generated_scripts
        self.generated_script_paths = []  # Track saved scripts
        
        if work_dir:
            self.work_dir = Path(work_dir)
            self.work_dir.mkdir(parents=True, exist_ok=True)
            self.cleanup_work_dir = False
        else:
            self.work_dir = Path(tempfile.mkdtemp(prefix="doc_tester_"))
            self.cleanup_work_dir = True
        
        if self.verbose:
            print(f"Working directory: {self.work_dir}")
    
    def _generate_script_filename(self, script_type: str, script_index: int = 0) -> str:
        """
        Generate a filename for the script following the _gen-<source>-<random>.<ext> pattern.
        
        Args:
            script_type: Type of script (bash, python, etc.)
            script_index: Index of the script
            
        Returns:
            Generated filename
        """
        # Determine extension
        if script_type.lower() in ['bash', 'sh']:
            extension = '.sh'
        elif script_type.lower() == 'python':
            extension = '.py'
        else:
            extension = f'.{script_type}'
        
        # Generate random suffix
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        # Sanitize source context for filename
        if self.source_context:
            # Convert path/URL to safe filename component
            sanitized = re.sub(r'[^\w\-.]', '_', self.source_context)
            # Remove leading/trailing underscores
            sanitized = sanitized.strip('_')
            # Limit length
            sanitized = sanitized[-50:] if len(sanitized) > 50 else sanitized
            filename = f"_gen-{sanitized}-{random_suffix}{extension}"
        else:
            filename = f"_gen-script{script_index}-{random_suffix}{extension}"
        
        return filename
    
    def execute_script(
        self,
        script_content: str,
        script_type: str = "bash",
        timeout: int = 600,
        env: Optional[Dict[str, str]] = None,
        script_index: int = 0
    ) -> Tuple[bool, str, str]:
        """
        Execute a script.
        
        Args:
            script_content: Content of the script to execute
            script_type: Type of script (bash, python, sh, etc.)
            timeout: Execution timeout in seconds
            env: Additional environment variables
            script_index: Index of the script (for naming)
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        # Determine script extension and interpreter
        if script_type.lower() in ['bash', 'sh']:
            extension = '.sh'
            interpreter = ['/bin/bash']
        elif script_type.lower() == 'python':
            extension = '.py'
            interpreter = ['python3']
        else:
            extension = f'.{script_type}'
            interpreter = None
        
        # Generate script filename
        if self.save_generated_scripts:
            script_filename = self._generate_script_filename(script_type, script_index)
            # Save in current directory for persistence
            script_path = Path.cwd() / script_filename
        else:
            # Use temp location
            script_path = self.work_dir / f"test_script{extension}"
        
        try:
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Track generated script
            if self.save_generated_scripts:
                self.generated_script_paths.append(str(script_path))
            
            # Make script executable for shell scripts
            if script_type.lower() in ['bash', 'sh']:
                os.chmod(script_path, 0o755)
            
            if self.verbose:
                print(f"\n{'='*60}")
                print(f"Executing {script_type} script: {script_path.name}")
                if self.save_generated_scripts:
                    print(f"Saved to: {script_path}")
                print(f"{'='*60}")
                print(script_content[:500] + ('...' if len(script_content) > 500 else ''))
                print(f"{'='*60}\n")
            
            # Prepare command
            if interpreter:
                cmd = interpreter + [str(script_path)]
            else:
                cmd = [str(script_path)]
            
            # Prepare environment
            exec_env = os.environ.copy()
            if env:
                exec_env.update(env)
            
            # Execute script
            result = subprocess.run(
                cmd,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=exec_env
            )
            
            success = result.returncode == 0
            
            if self.verbose:
                print(f"\n{'='*60}")
                print(f"Execution {'SUCCEEDED' if success else 'FAILED'} (exit code: {result.returncode})")
                print(f"{'='*60}")
                if result.stdout:
                    print("STDOUT:")
                    print(result.stdout)
                if result.stderr:
                    print("STDERR:")
                    print(result.stderr)
                print(f"{'='*60}\n")
            
            return success, result.stdout, result.stderr
        
        except subprocess.TimeoutExpired:
            error_msg = f"Script execution timed out after {timeout} seconds"
            if self.verbose:
                print(f"\n{'='*60}")
                print(f"ERROR: {error_msg}")
                print(f"{'='*60}\n")
            return False, "", error_msg
        
        except Exception as e:
            error_msg = f"Failed to execute script: {str(e)}"
            if self.verbose:
                print(f"\n{'='*60}")
                print(f"ERROR: {error_msg}")
                print(f"{'='*60}\n")
            return False, "", error_msg
    
    def execute_multiple_scripts(
        self,
        scripts: Dict[str, Dict[str, str]],
        stop_on_failure: bool = True
    ) -> Dict[str, Tuple[bool, str, str]]:
        """
        Execute multiple scripts in sequence.
        
        Args:
            scripts: Dictionary with script names as keys and dict with 'content' and 'type' as values
            stop_on_failure: Whether to stop execution if a script fails
            
        Returns:
            Dictionary with script names as keys and execution results as values
        """
        results = {}
        
        for idx, (script_name, script_info) in enumerate(scripts.items()):
            if self.verbose:
                print(f"\n{'#'*60}")
                print(f"# Executing: {script_name}")
                print(f"{'#'*60}\n")
            
            success, stdout, stderr = self.execute_script(
                script_info['content'],
                script_info.get('type', 'bash'),
                script_index=idx
            )
            
            results[script_name] = (success, stdout, stderr)
            
            if not success and stop_on_failure:
                if self.verbose:
                    print(f"\n[!] Stopping execution due to failure in: {script_name}")
                break
        
        return results
    
    def cleanup(self):
        """Clean up temporary working directory."""
        if self.cleanup_work_dir and self.work_dir.exists():
            try:
                shutil.rmtree(self.work_dir)
                if self.verbose:
                    print(f"Cleaned up working directory: {self.work_dir}")
            except Exception as e:
                print(f"Warning: Failed to cleanup working directory: {str(e)}")
        
        # Print summary of saved scripts
        if self.save_generated_scripts and self.generated_script_paths and self.verbose:
            print(f"\n{'='*60}")
            print(f"Generated scripts saved to:")
            for script_path in self.generated_script_paths:
                print(f"  - {script_path}")
            print(f"{'='*60}\n")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()

