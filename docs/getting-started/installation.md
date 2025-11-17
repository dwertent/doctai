---
layout: default
title: Installation
parent: Getting Started
nav_order: 1
---

# Installation

Install doctai on your system.

## Prerequisites

- **Python 3.8 or higher**
- pip (Python package manager)
- Internet connection (for AI API access)

Check your Python version:

```bash
python3 --version
```

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/dwertent/doctai.git
cd doctai

# Install in development mode
pip install -e .
```

### Verify Installation

```bash
doctai --help
```

You should see the help message with available options.

## Get an API Key

Choose one AI provider and get an API key:

### OpenAI

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy your API key

### Anthropic (Claude)

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Copy your API key

### Google Gemini

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Configure API Key

### Option 1: Environment Variable

Add to your shell configuration (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export DOCTAI_API_KEY=your-api-key-here
```

Or use provider-specific variables:

```bash
export ANTHROPIC_API_KEY=your-anthropic-key
export OPENAI_API_KEY=your-openai-key
export GEMINI_API_KEY=your-gemini-key
```

### Option 2: Configuration File

Create `.doctai.yml` in your project:

```yaml
provider: anthropic
model: claude-sonnet-4-20250514
api_key_env_var: ANTHROPIC_API_KEY

documentation_sources:
  - README.md
```

Then set the environment variable:

```bash
export ANTHROPIC_API_KEY=your-key
```

## Verify Setup

Test that everything works:

```bash
# Create a simple test file
echo "# Test\nRun: echo 'Hello World'" > test.md

# Run doctai
doctai --docs test.md --provider anthropic --api-key your-key

# Or if you set the environment variable:
doctai --docs test.md --provider anthropic
```

## Troubleshooting

### Command Not Found

If you get `doctai: command not found`:

```bash
# Make sure pip installed to a directory in your PATH
python3 -m pip install --user -e .

# Or add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Module Not Found

If you get module import errors:

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Issues

If you get authentication errors:

1. Verify your API key is correct
2. Check that the environment variable is set: `echo $DOCTAI_API_KEY`
3. Ensure you're using the correct provider name
4. Try passing the key directly with `--api-key`

## Next Steps

- [Quick Start](../getting-started.html) - Run your first test
- [Configuration Guide](../guides/configuration.html) - Set up `.doctai.yml`
- [GitHub Actions](../github-actions.html) - Automate testing
