---
layout: default
title: CLI Reference
parent: Reference
nav_order: 3
---

# Command-Line Interface Reference
{: .no_toc }

Complete reference for all doctai command-line options.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Basic Usage

```bash
doctai [OPTIONS]
```

## Required Options

### Documentation Sources

**Option:** `--docs`

Specify one or more documentation sources to test.

```bash
# Single file
doctai --docs README.md

# Multiple files
doctai --docs README.md --docs INSTALL.md

# URL
doctai --docs https://raw.githubusercontent.com/user/repo/main/README.md

# Directory (tests all markdown files)
doctai --docs docs/
```

**Alternative:** Use a configuration file (`.doctai.yml`) to specify sources.

## AI Provider Options

### --provider

Select which AI provider to use.

**Choices:** `openai`, `anthropic`, `gemini`, `custom`

```bash
doctai --docs README.md --provider anthropic
```

**Default:** `openai` (or from config file)

### --api-key

Your API key for the AI provider.

```bash
doctai --docs README.md --api-key sk-...
```

**Alternative methods:**
1. Environment variable: `export DOCTAI_API_KEY=your-key`
2. Config file: `api_key_env_var: ANTHROPIC_API_KEY`
3. Provider-specific env vars: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`

### --model

Specify which AI model to use.

```bash
# OpenAI
doctai --provider openai --model gpt-4

# Anthropic
doctai --provider anthropic --model claude-sonnet-4-20250514

# Gemini
doctai --provider gemini --model gemini-1.5-pro-latest
```

**Defaults:**
- OpenAI: `gpt-4`
- Anthropic: `claude-sonnet-4-20250514`
- Gemini: `gemini-1.5-pro-latest`

### --api-url

Custom API endpoint (for `custom` provider or OpenAI-compatible endpoints).

```bash
doctai --provider custom \
        --api-url https://api.example.com/v1 \
        --api-key your-key
```

## Configuration Options

### --config

Path to configuration file.

```bash
doctai --config .doctai.local.yml
```

**Default:** Searches for `.doctai.yml`, `.doctai.yaml`, or `.doctai.json` in current directory.

### --instructions

Provide custom instructions to guide the AI's testing behavior.

```bash
doctai --docs README.md \
        --instructions "Focus on testing the installation steps only"
```

**Alternative:** Add to config file:

```yaml
instructions: |
  Focus on testing the installation steps.
  Skip any optional features.
```

## Execution Options

### --max-iterations

Maximum number of AI conversation iterations.

```bash
doctai --docs README.md --max-iterations 5
```

**Default:** `3`

### --stop-on-failure

Stop executing scripts if one fails.

```bash
doctai --docs README.md --stop-on-failure
```

**Default:** `false` (continues even after failures)

### --work-dir

Specify a working directory for script execution.

```bash
doctai --docs README.md --work-dir /tmp/test
```

**Default:** Creates a temporary directory

## Output Options

### --verbose / --quiet

Control output verbosity.

```bash
# Verbose (detailed output)
doctai --docs README.md --verbose

# Quiet (minimal output)
doctai --docs README.md --quiet
```

**Default:** Verbose

## Examples

### Basic Test

```bash
doctai --docs README.md \
        --provider anthropic \
        --api-key sk-ant-...
```

### With Configuration File

```bash
# .doctai.yml contains provider, model, and docs
doctai
```

### Multiple Documentation Sources

```bash
doctai --docs README.md \
        --docs INSTALL.md \
        --docs docs/quickstart.md \
        --provider openai
```

### Custom Instructions

```bash
doctai --docs README.md \
        --provider anthropic \
        --instructions "Only test the Docker installation method"
```

### GitHub Actions

```bash
doctai --docs README.md \
        --provider anthropic \
        --api-key ${{ secrets.ANTHROPIC_API_KEY }} \
        --quiet
```

## Environment Variables

doctai respects the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DOCTAI_API_KEY` | Default API key | `export DOCTAI_API_KEY=sk-...` |
| `DOCTAI_API_KEY_ENV_VAR` | Name of env var containing API key | `export DOCTAI_API_KEY_ENV_VAR=OPENAI_API_KEY` |
| `OPENAI_API_KEY` | OpenAI-specific key | `export OPENAI_API_KEY=sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic-specific key | `export ANTHROPIC_API_KEY=sk-ant-...` |
| `GEMINI_API_KEY` | Gemini-specific key | `export GEMINI_API_KEY=AI...` |

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All tests passed |
| `1` | One or more tests failed |
| `2` | Configuration error |
| `3` | Authentication error |

## Configuration File Reference

See [Configuration Guide](../guides/configuration.html) for complete `.doctai.yml` reference.

## See Also

- [Quick Start Guide](../getting-started/quickstart.html)
- [Configuration Guide](../guides/configuration.html)
- [API Key Configuration](../api-key-configuration.html)

