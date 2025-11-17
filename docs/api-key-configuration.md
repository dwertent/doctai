---
layout: default
title: API Key Configuration
nav_order: 5
---

# API Key Configuration
{: .no_toc }

The doc-tester provides flexible ways to configure which environment variable contains your API key.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Default Behavior

By default, the tool reads the API key from the `DOC_TESTER_API_KEY` environment variable:

```bash
export DOC_TESTER_API_KEY="your-api-key-here"
doc-tester --docs README.md
```

## Using Provider-Specific Environment Variables

If you prefer to use provider-specific environment variables (e.g., `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`), you can configure this in your `.doc-tester.yml` file:

### Method 1: Config File (Recommended)

Add the `api_key_env_var` field to your config file:

```yaml
# .doc-tester.yml
provider: anthropic
model: claude-sonnet-4-20250514
api_key_env_var: ANTHROPIC_API_KEY
```

Then set your provider-specific environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
doc-tester
```

The tool will automatically read from `ANTHROPIC_API_KEY` instead of `DOC_TESTER_API_KEY`.

### Method 2: Environment Variable

You can also specify which environment variable to use via `DOC_TESTER_API_KEY_ENV_VAR`:

```bash
export OPENAI_API_KEY="sk-..."
export DOC_TESTER_API_KEY_ENV_VAR=OPENAI_API_KEY
doc-tester --docs README.md
```

## Multiple Setups / Projects

This feature is particularly useful when working with multiple projects that use different AI providers:

### Project A (Using Claude):
```yaml
# projectA/.doc-tester.yml
provider: anthropic
api_key_env_var: ANTHROPIC_API_KEY
```

```bash
cd projectA
export ANTHROPIC_API_KEY="sk-ant-..."
doc-tester
```

### Project B (Using OpenAI):
```yaml
# projectB/.doc-tester.yml
provider: openai
api_key_env_var: OPENAI_API_KEY
```

```bash
cd projectB
export OPENAI_API_KEY="sk-..."
doc-tester
```

### Project C (Using Gemini):
```yaml
# projectC/.doc-tester.yml
provider: gemini
api_key_env_var: GEMINI_API_KEY
```

```bash
cd projectC
export GEMINI_API_KEY="..."
doc-tester
```

## Priority Order

The tool checks for the API key in the following order:

1. **Command-line argument**: `--api-key YOUR_KEY` (highest priority)
2. **Specified environment variable**: From config file or `DOC_TESTER_API_KEY_ENV_VAR`
3. **Default environment variable**: `DOC_TESTER_API_KEY` (fallback)

## Examples

### Example 1: Using Standard Environment Variables

Many developers already have environment variables like `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` set up. Just configure the tool to use them:

```yaml
# .doc-tester.yml
provider: openai
model: gpt-4o
api_key_env_var: OPENAI_API_KEY
```

### Example 2: Different Keys for Different Environments

```bash
# Development
export DEV_API_KEY="sk-dev-..."

# Production
export PROD_API_KEY="sk-prod-..."

# In dev config
# .doc-tester.yml
api_key_env_var: DEV_API_KEY

# In prod config
# .doc-tester.prod.yml
api_key_env_var: PROD_API_KEY
```

### Example 3: CI/CD with GitHub Actions

```yaml
# .github/workflows/test-docs.yml
name: Test Documentation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Test Documentation
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          pip install -e .
          doc-tester
```

With config:
```yaml
# .doc-tester.yml
provider: anthropic
api_key_env_var: ANTHROPIC_API_KEY
```

## Supported Config Keys

The following config keys are recognized (in order of precedence):
- `api_key_env_var`
- `api_key_env`
- `api_key_var`

All three work the same way - use whichever you prefer.

## Troubleshooting

If the API key is not being found:

1. **Check environment variable name**:
   ```bash
   echo $ANTHROPIC_API_KEY  # Should print your key
   ```

2. **Check config file**:
   ```bash
   cat .doc-tester.yml | grep api_key_env_var
   ```

3. **Run with verbose output**:
   ```bash
   doc-tester --docs README.md
   # Should print: "Using API key from environment variable: ANTHROPIC_API_KEY"
   ```

4. **Test with explicit key** (for debugging):
   ```bash
   doc-tester --docs README.md --api-key "your-key"
   ```

