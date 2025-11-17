# Sample Project Setup Guide

This is an example documentation file that can be tested with the Documentation Tester.

## Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Create a virtual environment

```bash
python3 -m venv myenv
source myenv/bin/activate  # On Linux/Mac
# myenv\Scripts\activate  # On Windows
```

### Step 2: Install dependencies

Create a `requirements.txt` file with:

```
requests==2.31.0
```

Then install:

```bash
pip install -r requirements.txt
```

### Step 3: Create a simple script

Create a file called `test_app.py`:

```python
import requests

def test_api():
    """Test a simple API call."""
    response = requests.get('https://api.github.com')
    print(f"Status: {response.status_code}")
    return response.status_code == 200

if __name__ == '__main__':
    success = test_api()
    print(f"Test {'passed' if success else 'failed'}!")
    exit(0 if success else 1)
```

### Step 4: Run the script

```bash
python test_app.py
```

You should see output indicating the test passed.

## Verification

To verify everything is working:

```bash
python -c "import requests; print('Success!')"
```

## Cleanup

When done, deactivate the virtual environment:

```bash
deactivate
```

