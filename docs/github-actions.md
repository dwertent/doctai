---
layout: default
title: GitHub Actions
parent: Guides
nav_order: 5
---

# Using doctai in GitHub Actions
{: .no_toc }

Automate your documentation testing with GitHub Actions.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Quick Setup

### 1. Create Workflow File

Create `.github/workflows/test-docs.yml`:

```yaml
name: Test Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      docs:
        description: 'Documentation path/URL to test'
        required: false
        type: string

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
        run: |
          pip install doctai
          # Or install from source:
          # git clone https://github.com/dwertent/doctai.git
          # cd doctai
          # pip install -e .
      
      - name: Test Documentation
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          doctai --docs README.md --provider anthropic
```

### 2. Add API Key Secret

1. Go to your repository settings
2. Navigate to **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`, `GEMINI_API_KEY`)
5. Value: Your API key
6. Click **Add secret**

### 3. Test It

Push your changes or manually trigger the workflow from the Actions tab.

## Configuration-Based Setup

If you have a `.doctai.yml` file in your repository:

```yaml
name: Test Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

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
        run: doctai  # Uses .doctai.yml automatically
```

## Advanced Workflows

### Test Multiple Providers

```yaml
name: Test Documentation (Multi-Provider)

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  test-docs:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        provider: [openai, anthropic, gemini]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install doctai
        run: pip install doctai
      
      - name: Test with ${{ matrix.provider }}
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          doctai --docs README.md --provider ${{ matrix.provider }}
```

### Test Multiple Documents

```yaml
name: Test All Documentation

on:
  push:
    branches: [main]
    paths:
      - '**.md'
      - 'docs/**'

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
      
      - name: Test README
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: doctai --docs README.md --provider anthropic
      
      - name: Test Installation Guide
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: doctai --docs INSTALL.md --provider anthropic
      
      - name: Test Quick Start
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: doctai --docs docs/quickstart.md --provider anthropic
```

### Manual Trigger with Input

```yaml
name: Test Specific Documentation

on:
  workflow_dispatch:
    inputs:
      docs:
        description: 'Documentation path or URL'
        required: true
        type: string
      provider:
        description: 'AI Provider'
        required: true
        type: choice
        options:
          - openai
          - anthropic
          - gemini

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
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          doctai --docs "${{ inputs.docs }}" --provider "${{ inputs.provider }}"
```

## Best Practices

### 1. Use Configuration Files

Store settings in `.doctai.yml` to keep workflows clean:

```yaml
# .doctai.yml
provider: anthropic
model: claude-sonnet-4-20250514
api_key_env_var: ANTHROPIC_API_KEY

documentation_sources:
  - README.md
  - INSTALL.md
  - docs/quickstart.md
```

### 2. Protect Secrets

- Never commit API keys to your repository
- Use GitHub Secrets for all sensitive data
- Consider using environment-specific secrets for different branches

### 3. Optimize Costs

```yaml
# Only test on main branch and PRs
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    paths:
      - '**.md'  # Only when markdown files change
      - '.doctai.yml'
```

### 4. Cache Dependencies

```yaml
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### 5. Report Results

```yaml
- name: Test Documentation
  id: test
  continue-on-error: true
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: doctai --docs README.md --provider anthropic

- name: Comment on PR
  if: github.event_name == 'pull_request' && steps.test.outcome == 'failure'
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '⚠️ Documentation tests failed. Please review the changes.'
      })
```

## Troubleshooting

### Issue: API Key Not Found

**Error:** `API key not provided`

**Solution:**
1. Check that the secret is named correctly
2. Verify the secret is available in the workflow environment
3. Ensure you're using the correct environment variable name

```yaml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}  # Make sure this matches
```

### Issue: doctai Not Found

**Error:** `doctai: command not found`

**Solution:** Install doctai in the workflow:

```yaml
- name: Install doctai
  run: pip install doctai
```

### Issue: Tests Timeout

**Error:** `The job running on runner ... has exceeded the maximum execution time`

**Solution:** Reduce test scope or increase timeout:

```yaml
jobs:
  test-docs:
    timeout-minutes: 30  # Increase from default 360
    runs-on: ubuntu-latest
```

## Example Repository

See [doctai repository](https://github.com/dwertent/doctai) for working examples.

## See Also

- [Configuration Guide](configuration.html)
- [API Key Configuration](../api-key-configuration.html)
- [CLI Reference](../cli-reference.html)

