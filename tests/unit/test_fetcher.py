"""
Unit tests for the documentation fetcher.
"""

import pytest
from pathlib import Path
from doc_tester.fetcher import DocumentationFetcher


class TestDocumentationFetcher:
    """Test the DocumentationFetcher class."""
    
    def test_fetch_single_file(self, temp_dir, sample_doc):
        """Test fetching a single documentation file."""
        # Create test file
        doc_file = temp_dir / "README.md"
        doc_file.write_text(sample_doc)
        
        # Fetch documentation
        fetcher = DocumentationFetcher()
        result = fetcher.fetch(str(doc_file))
        
        # Verify
        assert len(result) == 1
        assert str(doc_file) in result
        assert "# Sample Documentation" in result[str(doc_file)]
    
    def test_fetch_directory(self, temp_dir):
        """Test fetching documentation from a directory."""
        # Create multiple doc files
        (temp_dir / "README.md").write_text("# README")
        (temp_dir / "INSTALL.md").write_text("# Installation")
        (temp_dir / "other.txt").write_text("# Other")
        (temp_dir / "code.py").write_text("print('hello')")  # Should be ignored
        
        # Fetch documentation
        fetcher = DocumentationFetcher()
        result = fetcher.fetch(str(temp_dir))
        
        # Verify - should find .md and .txt files only
        assert len(result) >= 2  # At least README and INSTALL
        assert any("README" in content for content in result.values())
        assert any("Installation" in content for content in result.values())
    
    def test_fetch_nonexistent_file(self):
        """Test fetching a non-existent file raises error."""
        fetcher = DocumentationFetcher()
        
        with pytest.raises(ValueError, match="does not exist"):
            fetcher.fetch("/nonexistent/path/to/file.md")
    
    def test_fetch_empty_directory(self, temp_dir):
        """Test fetching from empty directory raises error."""
        fetcher = DocumentationFetcher()
        
        with pytest.raises(ValueError, match="No documentation files found"):
            fetcher.fetch(str(temp_dir))
    
    def test_is_url(self):
        """Test URL detection."""
        fetcher = DocumentationFetcher()
        
        assert fetcher._is_url("https://example.com/doc.md")
        assert fetcher._is_url("http://example.com/doc.md")
        assert not fetcher._is_url("/path/to/file.md")
        assert not fetcher._is_url("README.md")

