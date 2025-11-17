"""
Pytest configuration and shared fixtures.
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_doc():
    """Sample documentation content."""
    return """# Sample Documentation

## Installation

To install, run:

```bash
pip install requests
```

## Usage

Create a simple script:

```python
import requests
response = requests.get('https://api.github.com')
print(f"Status: {response.status_code}")
```

## Verification

Run the script to verify installation.
"""


@pytest.fixture
def sample_config():
    """Sample configuration."""
    return {
        'docs': ['README.md', 'docs/installation.md'],
        'provider': 'openai',
        'model': 'gpt-4o',
        'stop_on_failure': False,
        'max_iterations': 3,
        'timeout': 120
    }


@pytest.fixture
def mock_ai_response():
    """Mock AI response with test scripts."""
    return """I'll test this documentation by creating these scripts:

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

These scripts will verify the installation and test the example code.
"""

