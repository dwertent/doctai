---
layout: default
title: Quick Start
parent: Getting Started
nav_order: 2
---

# Quick Start Guide

Get started with doctai in 5 minutes!

## 1. Install

```bash
cd /Users/dwertent/kaleido/temp/test-docs
pip install -e .
```

## 2. Set Your API Key

Choose your AI provider and set the API key:

### Option A: OpenAI (Recommended)

```bash
export DOCTAI_API_KEY="sk-your-openai-api-key-here"
```

### Option B: Anthropic Claude

```bash
export DOCTAI_API_KEY="sk-ant-your-anthropic-api-key-here"
export DOCTAI_PROVIDER="anthropic"
```

### Option C: Google Gemini

```bash
export DOCTAI_API_KEY="your-gemini-api-key-here"
export DOCTAI_PROVIDER="gemini"
```

## 3. Test the Example Documentation

### Option A: Using the built-in config file

```bash
doctai --api-key $DOCTAI_API_KEY
```

This project has a `.doctai.yml` file that automatically specifies which docs to test!

### Option B: Specify docs manually

```bash
doctai --docs examples/sample-documentation.md --api-key $DOCTAI_API_KEY
```

### Option C: Use the convenience script

```bash
./examples/test-example.sh
```

## 4. Test Your Own Documentation

```bash
doctai --docs /path/to/your/README.md --api-key $DOCTAI_API_KEY
```

## 5. Use in GitHub Actions

Add this to `.github/workflows/test-docs.yml`:

```yaml
name: Test Documentation

on: [push, pull_request]

jobs:
  test-docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install doctai
    - run: doctai --docs README.md --api-key ${{ secrets.OPENAI_API_KEY }}
```

Don't forget to add your API key as a GitHub secret!

## What Happens?

1. **Fetch**: doctai reads your documentation
2. **Analyze**: AI understands what needs to be done
3. **Generate**: AI creates executable test scripts
4. **Execute**: Scripts are run in a safe environment
5. **Report**: You get clear pass/fail results

## Common Use Cases

### Test Installation Instructions

```bash
doctai --docs docs/installation.md --api-key $DOCTAI_API_KEY
```

### Test Multiple Documents

```bash
doctai --docs README.md docs/setup.md docs/tutorial.md --api-key $DOCTAI_API_KEY
```

### Test Documentation from URL

```bash
doctai --docs https://raw.githubusercontent.com/user/repo/main/README.md --api-key $DOCTAI_API_KEY
```

### Save Results to JSON

```bash
doctai --docs README.md --api-key $DOCTAI_API_KEY --output results.json
```

### Run Quietly (CI/CD)

```bash
doctai --docs README.md --api-key $DOCTAI_API_KEY --quiet
```

## Troubleshooting

### "No module named 'doc_tester'"

Make sure you installed the package:
```bash
pip install -e .
```

### "API key is required"

Set your API key:
```bash
export DOCTAI_API_KEY="your-key-here"
```

### "No test scripts were generated"

Your documentation might not contain actionable instructions. Try:
- Adding specific installation commands
- Including code examples
- Making instructions more explicit

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [examples/](examples/) for more examples
- Integrate into your CI/CD pipeline
- Star the repo if you find it useful! ⭐

## Support

- GitHub Issues: For bug reports and feature requests
- Discussions: For questions and community support

---

**Happy Testing!** 🚀

