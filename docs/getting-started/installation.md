---
layout: default
title: Installation
parent: Getting Started
nav_order: 1
---

# Installation Guide

Complete installation guide for Documentation Tester.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for AI API access)

## Installation Methods

### Method 1: Install from Source (Recommended for Development)

1. **Clone or download the repository**

```bash
cd /path/to/doc-tester
```

2. **Create a virtual environment** (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# Or on Windows:
# venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Install the package in editable mode**

```bash
pip install -e .
```

5. **Verify installation**

```bash
doc-tester --version
python test_installation.py
```

### Method 2: Install from PyPI (When Published)

```bash
pip install doc-tester
```

### Method 3: Install with pipx (Isolated Installation)

```bash
pipx install doc-tester
```

## Post-Installation Setup

### 1. Get an AI API Key

You need an API key from one of these providers:

#### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-`)

#### Anthropic
1. Go to https://console.anthropic.com/
2. Create an API key
3. Copy the key (starts with `sk-ant-`)

#### Google Gemini
1. Go to https://aistudio.google.com/app/apikey
2. Create an API key
3. Copy the key

### 2. Configure API Key

#### Option A: Environment Variable (Recommended)

Add to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
export DOC_TESTER_API_KEY="your-api-key-here"
export DOC_TESTER_PROVIDER="openai"  # or "anthropic"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

#### Option B: Pass via Command Line

```bash
doc-tester --docs README.md --api-key "your-api-key-here"
```

#### Option C: Create a Config File

Create `~/.doc-tester.env`:

```bash
DOC_TESTER_API_KEY=your-api-key-here
DOC_TESTER_PROVIDER=openai
DOC_TESTER_MODEL=gpt-4o
```

Then load it:
```bash
source ~/.doc-tester.env
```

### 3. Test Installation

Run the installation test:

```bash
python test_installation.py
```

Or test with the example:

```bash
doc-tester --docs examples/sample-documentation.md --api-key $DOC_TESTER_API_KEY
```

## Troubleshooting

### Python Version Issues

Check your Python version:
```bash
python3 --version
```

If it's less than 3.8, upgrade Python:
- **macOS**: `brew install python@3.11`
- **Ubuntu**: `sudo apt update && sudo apt install python3.11`
- **Windows**: Download from https://python.org

### pip Not Found

Install pip:
- **macOS**: `python3 -m ensurepip`
- **Ubuntu**: `sudo apt install python3-pip`
- **Windows**: Included with Python installer

### "Externally Managed Environment" Error

This is a safety feature on some systems. Use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Import Errors

Make sure you:
1. Activated your virtual environment
2. Installed dependencies: `pip install -r requirements.txt`
3. Installed the package: `pip install -e .`

### Permission Denied

On Linux/macOS, if you get permission errors:

```bash
chmod +x examples/test-example.sh
chmod +x test_installation.py
```

### API Key Issues

- Verify your key is correct
- Check you have API credits/quota
- Ensure the key hasn't expired
- Try regenerating the key

### Network Issues

If you have a proxy or firewall:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

## Uninstallation

To remove Documentation Tester:

```bash
pip uninstall doc-tester
```

To also remove dependencies:

```bash
pip uninstall -r requirements.txt
```

## Upgrading

### From Source

```bash
git pull origin main
pip install -e . --upgrade
```

### From PyPI

```bash
pip install --upgrade doc-tester
```

## Development Setup

For contributors:

```bash
# Clone the repo
git clone https://github.com/yourusername/doc-tester.git
cd doc-tester

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e .
pip install pytest pytest-cov black flake8

# Run tests
python test_installation.py

# Format code
black doc_tester/

# Run linter
flake8 doc_tester/
```

## Docker Installation (Future)

Coming soon:

```bash
docker pull doc-tester:latest
docker run -e DOC_TESTER_API_KEY=$API_KEY doc-tester --docs README.md
```

## Platform-Specific Notes

### macOS

- Use Homebrew for Python: `brew install python@3.11`
- Virtual environments highly recommended
- May need to install Xcode Command Line Tools: `xcode-select --install`

### Linux

- Install Python 3.8+: `sudo apt install python3 python3-pip python3-venv`
- May need build tools: `sudo apt install build-essential`

### Windows

- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation
- Use PowerShell or Command Prompt
- Virtual environments recommended

## CI/CD Installation

For GitHub Actions, see `.github/workflows/test-docs.yml`

For other CI systems:

```bash
pip install doc-tester
# Or:
pip install -r requirements.txt && pip install -e .
```

## Getting Help

- **Documentation**: See README.md, QUICKSTART.md
- **Issues**: https://github.com/yourusername/doc-tester/issues
- **Discussions**: https://github.com/yourusername/doc-tester/discussions

---

**Happy Testing!** 🚀

