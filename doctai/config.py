"""
Configuration file handler for Documentation Tester.

Handles loading and parsing configuration files (YAML/JSON).
"""

import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path


class ConfigLoader:
    """Loads configuration from files."""
    
    DEFAULT_CONFIG_FILES = [
        ".doctai.yml",
        ".doctai.yaml",
        ".doctai.json",
        "doctai.yml",
        "doctai.yaml",
        "doctai.json",
    ]
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize config loader.
        
        Args:
            config_path: Optional path to config file. If not provided, searches for default files.
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Dictionary with configuration values
        """
        if self.config_path:
            # Load from specified path
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {self.config_path}")
            self.config = self._load_file(config_file)
        else:
            # Search for default config files
            self.config = self._find_and_load_default()
        
        return self.config
    
    def _find_and_load_default(self) -> Dict[str, Any]:
        """Find and load default config file."""
        # Check current directory first
        for filename in self.DEFAULT_CONFIG_FILES:
            config_file = Path(filename)
            if config_file.exists():
                return self._load_file(config_file)
        
        # No config file found, return empty config
        return {}
    
    def _load_file(self, config_file: Path) -> Dict[str, Any]:
        """Load config from a file."""
        suffix = config_file.suffix.lower()
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if suffix in ['.yml', '.yaml']:
                return self._parse_yaml(content)
            elif suffix == '.json':
                return json.loads(content)
            else:
                raise ValueError(f"Unsupported config file format: {suffix}")
        
        except Exception as e:
            raise RuntimeError(f"Failed to load config file {config_file}: {str(e)}")
    
    def _parse_yaml(self, content: str) -> Dict[str, Any]:
        """Parse YAML content."""
        try:
            import yaml
            return yaml.safe_load(content) or {}
        except ImportError:
            # If PyYAML not installed, try simple parsing for basic YAML
            return self._parse_simple_yaml(content)
    
    def _parse_simple_yaml(self, content: str) -> Dict[str, Any]:
        """
        Simple YAML parser for basic key-value pairs and lists.
        
        This is a fallback when PyYAML is not installed.
        Supports basic YAML syntax only.
        """
        config = {}
        current_list_key = None
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Check for list items
            if line.startswith('- '):
                if current_list_key:
                    if current_list_key not in config:
                        config[current_list_key] = []
                    config[current_list_key].append(line[2:].strip())
                continue
            
            # Check for key-value pairs
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if not value:
                    # This might be a list
                    current_list_key = key
                    config[key] = []
                else:
                    current_list_key = None
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    config[key] = value
        
        return config
    
    def get_docs(self) -> List[str]:
        """Get documentation sources from config."""
        if not self.config:
            return []
        
        # Support multiple key names
        for key in ['docs', 'documentation', 'sources', 'files']:
            if key in self.config:
                value = self.config[key]
                if isinstance(value, list):
                    return value
                elif isinstance(value, str):
                    # Single string, split by whitespace or commas
                    if ',' in value:
                        return [s.strip() for s in value.split(',') if s.strip()]
                    else:
                        return [s.strip() for s in value.split() if s.strip()]
        
        return []
    
    def get_provider(self) -> Optional[str]:
        """Get AI provider from config."""
        return self.config.get('provider') or self.config.get('ai_provider')
    
    def get_model(self) -> Optional[str]:
        """Get model name from config."""
        return self.config.get('model') or self.config.get('ai_model')
    
    def get_api_url(self) -> Optional[str]:
        """Get API URL from config."""
        return self.config.get('api_url') or self.config.get('api-url')
    
    def get_work_dir(self) -> Optional[str]:
        """Get working directory from config."""
        return self.config.get('work_dir') or self.config.get('work-dir')
    
    def get_stop_on_failure(self) -> bool:
        """Get stop-on-failure setting from config."""
        value = self.config.get('stop_on_failure') or self.config.get('stop-on-failure')
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', 'yes', '1', 'on']
        return False
    
    def get_max_iterations(self) -> Optional[int]:
        """Get max iterations from config."""
        value = self.config.get('max_iterations') or self.config.get('max-iterations')
        if value is not None:
            try:
                return int(value)
            except (ValueError, TypeError):
                pass
        return None
    
    def get_timeout(self) -> Optional[int]:
        """Get timeout from config."""
        value = self.config.get('timeout')
        if value is not None:
            try:
                return int(value)
            except (ValueError, TypeError):
                pass
        return None
    
    def get_instructions(self) -> Optional[str]:
        """Get custom instructions from config."""
        # Support multiple key names
        for key in ['instructions', 'custom_instructions', 'additional_instructions', 'notes']:
            if key in self.config:
                value = self.config[key]
                if isinstance(value, str):
                    return value
                elif isinstance(value, list):
                    # Join list items with newlines
                    return '\n'.join(str(item) for item in value)
        return None
    
    def get_api_key_env_var(self) -> Optional[str]:
        """Get the name of the environment variable containing the API key."""
        for key in ['api_key_env_var', 'api_key_env', 'api_key_var']:
            if key in self.config:
                value = self.config[key]
                if isinstance(value, str):
                    return value
        return None
    
    def merge_with_args(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge config with command-line arguments.
        
        Command-line arguments take precedence over config file.
        
        Args:
            args: Dictionary of command-line arguments
            
        Returns:
            Merged configuration
        """
        merged = {}
        
        # Start with config file values
        if not args.get('docs'):
            merged['docs'] = self.get_docs()
        else:
            merged['docs'] = args['docs']
        
        # Provider (CLI takes precedence)
        merged['provider'] = args.get('provider') or self.get_provider() or 'openai'
        
        # Model (CLI takes precedence)
        merged['model'] = args.get('model') or self.get_model()
        
        # API URL (CLI takes precedence)
        merged['api_url'] = args.get('api_url') or self.get_api_url()
        
        # Work dir (CLI takes precedence)
        merged['work_dir'] = args.get('work_dir') or self.get_work_dir()
        
        # Stop on failure (CLI takes precedence)
        if args.get('stop_on_failure') is not None:
            merged['stop_on_failure'] = args['stop_on_failure']
        else:
            merged['stop_on_failure'] = self.get_stop_on_failure()
        
        # Max iterations (CLI takes precedence)
        merged['max_iterations'] = args.get('max_iterations') or self.get_max_iterations() or 3
        
        # Timeout (CLI takes precedence)
        merged['timeout'] = args.get('timeout') or self.get_timeout() or 120
        
        # API key always from args/env
        merged['api_key'] = args.get('api_key')
        
        # Output file
        merged['output'] = args.get('output')
        
        # Verbose/quiet
        merged['quiet'] = args.get('quiet', False)
        
        # Custom instructions (CLI takes precedence)
        merged['instructions'] = args.get('instructions') or self.get_instructions()
        
        return merged

