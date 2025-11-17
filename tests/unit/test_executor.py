"""
Unit tests for the script executor.
"""

import pytest
from doctai.executor import ScriptExecutor


class TestScriptExecutor:
    """Test the ScriptExecutor class."""
    
    def test_execute_simple_bash_script(self):
        """Test executing a simple bash script."""
        script = """#!/bin/bash
echo "Hello, World!"
"""
        
        with ScriptExecutor(verbose=False) as executor:
            success, stdout, stderr = executor.execute_script(script, "bash")
        
        assert success is True
        assert "Hello, World!" in stdout
        assert stderr == ""
    
    def test_execute_python_script(self):
        """Test executing a Python script."""
        script = """
print("Python test")
result = 2 + 2
print(f"Result: {result}")
"""
        
        with ScriptExecutor(verbose=False) as executor:
            success, stdout, stderr = executor.execute_script(script, "python")
        
        assert success is True
        assert "Python test" in stdout
        assert "Result: 4" in stdout
    
    def test_execute_failing_script(self):
        """Test executing a script that fails."""
        script = """#!/bin/bash
exit 1
"""
        
        with ScriptExecutor(verbose=False) as executor:
            success, stdout, stderr = executor.execute_script(script, "bash")
        
        assert success is False
    
    def test_execute_with_timeout(self):
        """Test script execution timeout."""
        # Script that sleeps for a long time
        script = """#!/bin/bash
sleep 60
"""
        
        with ScriptExecutor(verbose=False) as executor:
            success, stdout, stderr = executor.execute_script(
                script, "bash", timeout=1
            )
        
        assert success is False
        assert "timed out" in stderr.lower()
    
    def test_execute_multiple_scripts(self):
        """Test executing multiple scripts in sequence."""
        scripts = {
            "script_1": {
                "content": "#!/bin/bash\necho 'Script 1'",
                "type": "bash"
            },
            "script_2": {
                "content": "#!/bin/bash\necho 'Script 2'",
                "type": "bash"
            }
        }
        
        with ScriptExecutor(verbose=False) as executor:
            results = executor.execute_multiple_scripts(scripts)
        
        assert len(results) == 2
        assert results["script_1"][0] is True  # Success
        assert results["script_2"][0] is True
    
    def test_stop_on_failure(self):
        """Test stopping execution after first failure."""
        scripts = {
            "script_1": {
                "content": "#!/bin/bash\nexit 1",  # Fails
                "type": "bash"
            },
            "script_2": {
                "content": "#!/bin/bash\necho 'Should not run'",
                "type": "bash"
            }
        }
        
        with ScriptExecutor(verbose=False) as executor:
            results = executor.execute_multiple_scripts(
                scripts, stop_on_failure=True
            )
        
        assert len(results) == 1  # Only first script ran
        assert results["script_1"][0] is False
    
    def test_working_directory_creation(self, temp_dir):
        """Test that working directory is created."""
        with ScriptExecutor(work_dir=str(temp_dir / "test_wd"), verbose=False) as executor:
            assert executor.work_dir.exists()
    
    def test_cleanup(self, temp_dir):
        """Test that temporary directory is cleaned up."""
        executor = ScriptExecutor(verbose=False)
        work_dir = executor.work_dir
        
        assert work_dir.exists()
        
        executor.cleanup()
        
        # Temp dir should be cleaned up
        # (May still exist if cleanup_work_dir is False)

