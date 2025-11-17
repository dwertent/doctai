"""
Unit tests for the configuration loader.
"""

import pytest
import yaml
from pathlib import Path
from doctai.config import ConfigLoader


class TestConfigLoader:
    """Test the ConfigLoader class."""
    
    def test_load_yaml_config(self, temp_dir, sample_config):
        """Test loading a YAML configuration file."""
        # Create config file
        config_file = temp_dir / ".doctai.yml"
        with open(config_file, 'w') as f:
            yaml.dump(sample_config, f)
        
        # Load config
        loader = ConfigLoader(str(config_file))
        config = loader.load()
        
        # Verify
        assert config['provider'] == 'openai'
        assert 'README.md' in config['docs']
    
    def test_get_docs(self, temp_dir):
        """Test extracting documentation sources."""
        config_file = temp_dir / ".doctai.yml"
        config_file.write_text("""
docs:
  - README.md
  - docs/installation.md
provider: openai
""")
        
        loader = ConfigLoader(str(config_file))
        loader.load()
        docs = loader.get_docs()
        
        assert len(docs) == 2
        assert "README.md" in docs
        assert "docs/installation.md" in docs
    
    def test_get_provider(self, temp_dir):
        """Test extracting AI provider."""
        config_file = temp_dir / ".doctai.yml"
        config_file.write_text("""
docs:
  - README.md
provider: gemini
""")
        
        loader = ConfigLoader(str(config_file))
        loader.load()
        
        assert loader.get_provider() == "gemini"
    
    def test_get_instructions(self, temp_dir):
        """Test extracting custom instructions."""
        config_file = temp_dir / ".doctai.yml"
        config_file.write_text("""
docs:
  - README.md
instructions: |
  Test on Ubuntu 22.04
  Skip Docker examples
""")
        
        loader = ConfigLoader(str(config_file))
        loader.load()
        instructions = loader.get_instructions()
        
        assert instructions is not None
        assert "Ubuntu 22.04" in instructions
        assert "Docker" in instructions
    
    def test_instructions_as_list(self, temp_dir):
        """Test instructions provided as a list."""
        config_file = temp_dir / ".doctai.yml"
        config_file.write_text("""
docs:
  - README.md
instructions:
  - Instruction 1
  - Instruction 2
  - Instruction 3
""")
        
        loader = ConfigLoader(str(config_file))
        loader.load()
        instructions = loader.get_instructions()
        
        assert "Instruction 1" in instructions
        assert "Instruction 2" in instructions
    
    def test_merge_with_args(self, temp_dir):
        """Test merging config with command-line arguments."""
        config_file = temp_dir / ".doctai.yml"
        config_file.write_text("""
docs:
  - README.md
provider: openai
model: gpt-4o
""")
        
        loader = ConfigLoader(str(config_file))
        loader.load()
        
        # CLI overrides config
        merged = loader.merge_with_args({
            'docs': ['INSTALL.md'],  # Override
            'provider': 'gemini',     # Override
            'model': None,            # Use config
            'api_url': None,
            'work_dir': None,
            'stop_on_failure': None,
            'max_iterations': None,
            'timeout': None,
            'api_key': 'test-key',
            'output': None,
            'quiet': False,
            'instructions': None
        })
        
        assert merged['docs'] == ['INSTALL.md']  # CLI wins
        assert merged['provider'] == 'gemini'    # CLI wins
        assert merged['model'] == 'gpt-4o'       # From config
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent config raises error."""
        loader = ConfigLoader("/nonexistent/config.yml")
        
        with pytest.raises(FileNotFoundError):
            loader.load()
    
    def test_auto_discover_config(self, temp_dir, monkeypatch):
        """Test auto-discovery of config file."""
        # Change to temp dir
        monkeypatch.chdir(temp_dir)
        
        # Create config file
        config_file = temp_dir / ".doctai.yml"
        config_file.write_text("""
docs:
  - README.md
provider: openai
""")
        
        # Load without specifying path
        loader = ConfigLoader()
        config = loader.load()
        
        assert config['provider'] == 'openai'

