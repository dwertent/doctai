"""
Documentation fetcher module.

Handles fetching documentation from various sources (local files, URLs, etc.)
"""

import os
import requests
from typing import List, Dict
from pathlib import Path
from urllib.parse import urlparse


class DocumentationFetcher:
    """Fetches documentation from files or URLs."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the documentation fetcher.
        
        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout
    
    def fetch(self, source: str) -> Dict[str, str]:
        """
        Fetch documentation from a source.
        
        Args:
            source: Path to file/directory or URL
            
        Returns:
            Dictionary with source path/URL as key and content as value
        """
        if self._is_url(source):
            return self._fetch_from_url(source)
        else:
            return self._fetch_from_path(source)
    
    def fetch_multiple(self, sources: List[str]) -> Dict[str, str]:
        """
        Fetch documentation from multiple sources.
        
        Args:
            sources: List of paths or URLs
            
        Returns:
            Dictionary with source identifiers as keys and content as values
        """
        all_docs = {}
        for source in sources:
            docs = self.fetch(source)
            all_docs.update(docs)
        return all_docs
    
    def _is_url(self, source: str) -> bool:
        """Check if source is a URL."""
        try:
            result = urlparse(source)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _fetch_from_url(self, url: str) -> Dict[str, str]:
        """Fetch documentation from a URL."""
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return {url: response.text}
        except Exception as e:
            raise ValueError(f"Failed to fetch documentation from URL {url}: {str(e)}")
    
    def _fetch_from_path(self, path: str) -> Dict[str, str]:
        """Fetch documentation from a local path (file or directory)."""
        path_obj = Path(path)
        
        if not path_obj.exists():
            raise ValueError(f"Path does not exist: {path}")
        
        if path_obj.is_file():
            return self._read_file(path_obj)
        elif path_obj.is_dir():
            return self._read_directory(path_obj)
        else:
            raise ValueError(f"Invalid path type: {path}")
    
    def _read_file(self, file_path: Path) -> Dict[str, str]:
        """Read a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {str(file_path): content}
        except Exception as e:
            raise ValueError(f"Failed to read file {file_path}: {str(e)}")
    
    def _read_directory(self, dir_path: Path) -> Dict[str, str]:
        """
        Read all documentation files from a directory.
        
        Looks for common documentation file extensions.
        """
        doc_extensions = {'.md', '.txt', '.rst', '.adoc', '.markdown'}
        docs = {}
        
        for file_path in dir_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in doc_extensions:
                try:
                    docs.update(self._read_file(file_path))
                except Exception as e:
                    print(f"Warning: Skipping {file_path}: {str(e)}")
        
        if not docs:
            raise ValueError(f"No documentation files found in directory: {dir_path}")
        
        return docs

