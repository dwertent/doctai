---
layout: default
title: Configuration
parent: Guides
nav_order: 1
---

# Configuration File Guide

doctai supports configuration files to make it easier to manage documentation sources and settings across your project.

## Quick Start

1. **Create a config file** in your project root:

```yaml
# .doctai.yml
docs:
  - README.md
  - docs/installation.md
  - docs/quickstart.md

provider: openai
```

2. **Run without specifying docs**:

```bash
doctai --api-key $API_KEY
```

The tool will automatically find and use your config file!

## Config File Formats

### YAML Format (Recommended)

**Filename**: `.doctai.yml` or `.doctai.yaml`

```yaml
# Documentation sources to test
docs:
  - README.md
  - docs/installation.md
  - docs/quickstart.md
  - https://example.com/remote-doc.md

# AI Provider
provider: openai

# Model (optional)
model: gpt-4o

# Working directory (optional)
work_dir: /tmp/doc-tests

# Stop on first failure (optional)
stop_on_failure: false

# Maximum AI iterations (optional)
max_iterations: 3

# Timeout in seconds (optional)
timeout: 120
```

## Config File Locations

The tool searches for config files in this order:

1. Path specified with `--config` flag
2. `.doctai.yml` (current directory)
3. `.doctai.yaml`
4. `doctai.yml`
5. `doctai.yaml`

**Recommended:** Use `.doctai.yml` in your project root.

## Configuration Options

### `docs` (required in config or CLI)

List of documentation sources to test.

**Supported types:**
- Local files: `README.md`
- Directories: `docs/`
- URLs: `https://example.com/docs.md`

**Example:**
```yaml
docs:
  - README.md
  - INSTALL.md
  - docs/
  - https://raw.githubusercontent.com/user/repo/main/README.md
```

**Alternative keys:** `documentation`, `sources`, `files`

### `provider` (optional, default: openai)

AI provider to use.

**Options:** `openai`, `anthropic`, `gemini`, `custom`

```yaml
provider: gemini
```

### `api_key_env_var` (optional, default: DOCTAI_API_KEY)

Specifies which environment variable contains your API key.

**Why use this?** Useful when:
- You want to use provider-specific environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)
- You have different API keys for different environments
- You're working with multiple projects that use different providers

```yaml
provider: anthropic
api_key_env_var: ANTHROPIC_API_KEY
```

Then set the environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
doctai
```

**Alternative keys:** `api_key_env`, `api_key_var`

See the [API Key Configuration](../api-key-configuration.md) page for detailed examples.

### `model` (optional)

Specific model to use. If not specified, uses provider default.

**Examples:**
```yaml
# OpenAI
model: gpt-4o

# Anthropic
model: claude-3-5-sonnet-20241022

# Gemini
model: gemini-1.5-pro-latest
```

**Alternative key:** `ai_model`

### `api_url` (optional)

Custom API endpoint (required for custom provider).

```yaml
api_url: https://your-api.com/v1/chat
```

**Alternative key:** `api-url`

### `work_dir` (optional)

Working directory for script execution.

```yaml
work_dir: /tmp/doc-tests
```

**Alternative key:** `work-dir`

### `stop_on_failure` (optional, default: false)

Stop executing scripts after first failure.

```yaml
stop_on_failure: true
```

**Alternative key:** `stop-on-failure`

### `max_iterations` (optional, default: 3)

Maximum AI conversation iterations.

```yaml
max_iterations: 5
```

**Alternative key:** `max-iterations`

### `timeout` (optional, default: 120)

AI request timeout in seconds.

```yaml
timeout: 180
```

### `instructions` (optional)

Custom instructions to provide additional context or guidance to the AI.

This is useful for:
- Specifying which parts of documentation to focus on
- Providing environment-specific requirements
- Indicating what to skip or emphasize
- Giving context about specific test scenarios

**As a string:**
```yaml
instructions: "Test on Ubuntu 22.04. Use Python 3.10+. Skip Docker examples."
```

**As a multi-line string:**
```yaml
instructions: |
  - Focus on the installation guide
  - Use the test API endpoint: https://api.test.example.com
  - Skip examples requiring database connections
  - Test both pip and conda installation methods
```

**As a list:**
```yaml
instructions:
  - Test installation on Ubuntu 22.04
  - Use Python 3.10 or higher
  - Skip Docker-related examples
  - Focus on core functionality first
```

**Alternative keys:** `custom_instructions`, `additional_instructions`, `notes`

## Command-Line Override

Command-line arguments always take precedence over config file settings.

```bash
# Config file has: docs: [README.md]
# This overrides to test INSTALL.md instead:
doctai --docs INSTALL.md --api-key $API_KEY
```

**Override order (highest to lowest priority):**
1. Command-line arguments
2. Config file
3. Default values

## Usage Examples

### Example 1: Simple Config

```yaml
# .doctai.yml
docs:
  - README.md
  - INSTALL.md

provider: openai
```

```bash
# Uses config file
doctai --api-key $OPENAI_API_KEY
```

### Example 2: Override Provider

```yaml
# .doctai.yml
docs:
  - README.md

provider: openai
```

```bash
# Uses docs from config, but switches to Gemini
doctai --api-key $GEMINI_API_KEY --provider gemini
```

### Example 3: Custom Config Location

```yaml
# config/doc-test.yml
docs:
  - README.md
```

```bash
doctai --config config/doc-test.yml --api-key $API_KEY
```

### Example 4: Multiple Environments

**Development config:**
```yaml
# .doctai.yml
docs:
  - README.md
  - docs/development.md

provider: gemini  # Cheaper for testing
model: gemini-1.5-flash-latest
```

**Production config:**
```yaml
# .doctai.production.yml
docs:
  - README.md
  - docs/installation.md
  - docs/api.md
  - docs/tutorial.md

provider: openai
model: gpt-4o
stop_on_failure: true
```

```bash
# Development
doctai --api-key $GEMINI_API_KEY

# Production
doctai --config .doctai.production.yml --api-key $OPENAI_API_KEY
```

## GitHub Actions Integration

### Automatic Config Loading

The workflow will automatically use your config file when no docs are specified:

```yaml
# .doctai.yml in your repo
docs:
  - README.md
  - docs/installation.md
```

Workflow will use these automatically on push/PR:

```yaml
name: Test Documentation
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install doctai
      - run: doctai --api-key ${{ secrets.OPENAI_API_KEY }}
```

### Manual Override

You can still override via workflow dispatch:

1. Go to Actions → Test Documentation
2. Click "Run workflow"
3. Enter different docs: `README.md CONTRIBUTING.md`
4. Run

The specified docs will override the config file.

## Best Practices

### 1. ✅ Commit Config Files

Commit `.doctai.yml` to your repository:
- ✅ Makes testing consistent across team
- ✅ Documents what gets tested
- ✅ Works automatically in CI/CD

```bash
git add .doctai.yml
git commit -m "Add doctai configuration"
```

### 2. ⚠️ Never Store API Keys in Config

```yaml
# ❌ NEVER DO THIS
api_key: sk-1234567890abcdef  # DANGEROUS!

# ✅ DO THIS INSTEAD
# Use environment variables or secrets
# (no api_key in config file)
```

### 3. 📁 Use Local Configs for Personal Settings

Create a local config that won't be committed:

```yaml
# .doctai.local.yml (gitignored)
provider: gemini  # Your preference
model: gemini-1.5-flash-latest
work_dir: /tmp/my-tests
```

```bash
doctai --config .doctai.local.yml --api-key $API_KEY
```

### 4. 📝 Document Your Config

```yaml
# .doctai.yml
# This config tests our main user-facing documentation
# Run with: doctai --api-key $OPENAI_API_KEY

docs:
  - README.md        # Main project readme
  - INSTALL.md       # Installation guide
  - docs/tutorial.md # Getting started tutorial

provider: openai
max_iterations: 3
```

### 5. 🔄 Different Configs for Different Purposes

```bash
# Quick local testing (cheap, fast)
.doctai.yml               # Uses Gemini Flash

# CI/CD testing (thorough)
.doctai.ci.yml           # Uses GPT-4o

# Release testing (comprehensive)
.doctai.release.yml      # Tests all docs
```

## Troubleshooting

### "No documentation sources specified"

**Problem:** No `--docs` argument and config file not found or has no `docs` field.

**Solution:**
1. Create `.doctai.yml` with `docs` field
2. Or specify `--docs` on command line
3. Or use `--config` to point to your config file

### "Config file not found"

**Problem:** Specified config file doesn't exist.

```bash
doctai --config missing.yml --api-key $API_KEY
```

**Solution:**
- Check the file path is correct
- Ensure file exists
- Use relative or absolute path

### Config File Ignored

**Problem:** CLI arguments override config.

```bash
# Config has: docs: [README.md]
doctai --docs INSTALL.md  # Ignores config docs
```

**Solution:** This is expected behavior. CLI always wins. Remove CLI arg to use config.

### YAML Parsing Errors

**Problem:** Complex YAML not supported without PyYAML.

**Solution:**
```bash
# Install PyYAML for full YAML support
pip install pyyaml
```

Or use simple YAML syntax:
```yaml
# Simple format (works without PyYAML)
docs:
  - README.md
  - INSTALL.md
provider: openai
model: gpt-4o
```

## Examples Repository

See the [examples directory](examples/) for more config file examples:

- `.doctai.example.yml` - YAML template
- `.doctai.example.json` - JSON template
- `.doctai.yml` - Working example for this project

## Migration from CLI-only

**Before (CLI only):**
```bash
doctai \
  --docs README.md docs/install.md docs/tutorial.md \
  --provider openai \
  --model gpt-4o \
  --max-iterations 3 \
  --api-key $OPENAI_API_KEY
```

**After (with config):**

```yaml
# .doctai.yml
docs:
  - README.md
  - docs/install.md
  - docs/tutorial.md
provider: openai
model: gpt-4o
max_iterations: 3
```

```bash
doctai --api-key $OPENAI_API_KEY
```

Much cleaner! 🎉

## Summary

- ✅ Config files make documentation testing easier
- ✅ Supports YAML and JSON formats
- ✅ Auto-discovery of config files
- ✅ CLI arguments override config
- ✅ Perfect for CI/CD automation
- ✅ Never store API keys in config
- ✅ Commit configs to your repo

---

**Ready to start?**

```bash
# 1. Create config
echo "docs:\n  - README.md\nprovider: openai" > .doctai.yml

# 2. Test it
doctai --api-key $OPENAI_API_KEY

# 3. Commit it
git add .doctai.yml
git commit -m "Add documentation testing config"
```

For more information, see the [README](README.md) and [QUICKSTART](QUICKSTART.md).

