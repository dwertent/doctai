"""
Mock objects and responses for testing.
"""

# Mock AI responses for different scenarios
VALID_AI_RESPONSE = """I'll test this documentation by creating these scripts:

```bash
#!/bin/bash
set -e

# Install dependencies
pip install requests

# Verify installation
python -c "import requests; print('Installation successful!')"
```

```python
# Test the example code
import requests

def test_api_call():
    response = requests.get('https://api.github.com')
    assert response.status_code == 200
    print(f"API call successful: {response.status_code}")

if __name__ == '__main__':
    test_api_call()
```

These scripts will verify the installation instructions and test the example code from the documentation.
"""

NO_SCRIPTS_RESPONSE = """The documentation looks good but I cannot extract any executable code 
from it. It appears to be purely informational."""

MALFORMED_RESPONSE = """This response doesn't contain properly formatted code blocks
and cannot be parsed correctly."""

COMPLEX_AI_RESPONSE = """I'll create a comprehensive test suite:

```bash
#!/bin/bash
# Setup script
echo "Setting up environment..."
pip install -r requirements.txt
```

```python
# Test script 1
import sys
print(f"Python version: {sys.version}")
```

```bash
# Verification script
python --version
pip list
```

```python
# Final test
print("All tests passed!")
```

This will test the complete setup process.
"""


def mock_openai_response(content: str = VALID_AI_RESPONSE):
    """Generate a mock OpenAI API response."""
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": content
            }
        }],
        "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 200,
            "total_tokens": 300
        }
    }


def mock_anthropic_response(content: str = VALID_AI_RESPONSE):
    """Generate a mock Anthropic API response."""
    return {
        "content": [{
            "type": "text",
            "text": content
        }],
        "usage": {
            "input_tokens": 100,
            "output_tokens": 200
        }
    }


def mock_gemini_response(content: str = VALID_AI_RESPONSE):
    """Generate a mock Gemini API response."""
    return {
        "candidates": [{
            "content": {
                "parts": [{
                    "text": content
                }]
            }
        }]
    }

