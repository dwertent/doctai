---
layout: default
title: Features
parent: Guides
nav_order: 1
---

# Features Overview

Complete guide to doctai's capabilities.

## Core Features

### 🤖 AI-Powered Testing

doctai uses advanced AI models to:
- **Understand** your documentation like a human would
- **Generate** executable test scripts (bash, Python, etc.)
- **Verify** that instructions actually work

**Supported AI Providers:**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude Sonnet, Claude Opus)
- Google Gemini
- Custom OpenAI-compatible endpoints

### 📄 Flexible Documentation Sources

Test documentation from multiple sources:

```bash
# Local files
doctai --docs README.md

# Multiple files
doctai --docs README.md --docs INSTALL.md

# Remote URLs
doctai --docs https://raw.githubusercontent.com/user/repo/main/README.md

# Entire directories
doctai --docs docs/
```

### ⚙️ Configuration Files

Create a `.doctai.yml` file to avoid repetitive command-line flags:

```yaml
provider: anthropic
model: claude-sonnet-4-20250514
api_key_env_var: ANTHROPIC_API_KEY

documentation_sources:
  - README.md
  - INSTALL.md
  - docs/quickstart.md

instructions: |
  Focus on testing installation steps.
  Skip optional features.
```

Then simply run:

```bash
doctai
```

[Learn more about configuration →](configuration.html)

### 🎯 Custom Instructions

Guide the AI's testing behavior:

```bash
doctai --docs README.md \
        --instructions "Only test the Docker installation method"
```

Or in your config file:

```yaml
instructions: |
  Focus on testing the basic installation.
  Test on Ubuntu 22.04.
  Skip Windows-specific steps.
```

[Learn more about custom instructions →](instructions.html)

### 💾 Generated Script Saving

All generated scripts are saved to disk for inspection:

```bash
doctai --docs README.md --provider anthropic
# Creates: _gen-README.md-abc123.sh
```

Scripts are named based on:
- Source documentation filename
- AI-suggested filename (from script comments)
- Random suffix for uniqueness

**Benefits:**
- Debug test failures
- Understand what the AI generated
- Reuse scripts manually
- Learn from AI-generated code

### 🔑 Flexible API Key Configuration

Multiple ways to provide API keys:

**1. Environment Variable (Recommended)**
```bash
export DOCTAI_API_KEY=your-key
doctai --docs README.md
```

**2. Provider-Specific Variables**
```bash
export ANTHROPIC_API_KEY=your-key
export OPENAI_API_KEY=your-key
export GEMINI_API_KEY=your-key
```

**3. Config File**
```yaml
api_key_env_var: ANTHROPIC_API_KEY
```

**4. Command Line**
```bash
doctai --docs README.md --api-key your-key
```

[Learn more about API key configuration →](../api-key-configuration.html)

### 🔄 GitHub Actions Integration

Automate documentation testing in CI/CD:

```yaml
name: Test Documentation

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install doctai
        run: pip install doctai
      
      - name: Test Documentation
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: doctai --docs README.md --provider anthropic
```

[Learn more about GitHub Actions →](../github-actions.html)

## Advanced Features

### Script Execution Control

Control how scripts are executed:

```bash
# Stop on first failure
doctai --docs README.md --stop-on-failure

# Custom working directory
doctai --docs README.md --work-dir /tmp/test

# Adjust AI iterations
doctai --docs README.md --max-iterations 5
```

### Verbose and Quiet Modes

```bash
# Detailed output (default)
doctai --docs README.md --verbose

# Minimal output
doctai --docs README.md --quiet
```

### Custom AI Models

Use specific models:

```bash
# OpenAI GPT-4
doctai --provider openai --model gpt-4

# Anthropic Claude Opus
doctai --provider anthropic --model claude-3-opus-20240229

# Google Gemini Pro
doctai --provider gemini --model gemini-1.5-pro-latest
```

### Custom API Endpoints

Use OpenAI-compatible endpoints:

```bash
doctai --provider custom \
        --api-url https://api.example.com/v1 \
        --api-key your-key
```

## Use Cases

### 📝 Test Installation Guides

Verify that your installation instructions actually work:

```bash
doctai --docs INSTALL.md
```

### 🚀 Test Quick Start Tutorials

Ensure your quick start guide doesn't have broken steps:

```bash
doctai --docs docs/quickstart.md
```

### 🔧 Test Setup Documentation

Validate complex setup procedures:

```bash
doctai --docs docs/setup.md \
        --instructions "Test the manual installation method"
```

### 📚 Test API Examples

Verify that code examples in your API documentation work:

```bash
doctai --docs docs/api/examples.md
```

### 🐳 Test Docker Workflows

Ensure Docker setup instructions are correct:

```bash
doctai --docs docker/README.md \
        --instructions "Focus on Docker Compose setup"
```

## Best Practices

### 1. Use Configuration Files

Store common settings in `.doctai.yml` to avoid repetition.

### 2. Test Regularly

Add doctai to your CI/CD pipeline to catch documentation issues early.

### 3. Provide Custom Instructions

Guide the AI to test what matters most for your project.

### 4. Review Generated Scripts

Check saved scripts to understand what the AI is testing.

### 5. Start Simple

Begin with a single README.md, then expand to more documentation.

## Limitations

- Requires valid API keys for AI providers
- May incur API costs depending on usage
- Generated scripts might need environment setup
- Best for procedural documentation (installation, setup, tutorials)
- May not work well for conceptual or reference documentation

## See Also

- [Configuration Guide](configuration.html)
- [CLI Reference](../cli-reference.html)
- [GitHub Actions Guide](../github-actions.html)
