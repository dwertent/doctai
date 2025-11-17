---
layout: default
title: Getting Started
nav_order: 2
has_children: true
---

# Getting Started

Get up and running with doctai in minutes.

## Installation

**Python 3.8+ required**

```bash
git clone https://github.com/dwertent/doctai.git
cd doctai
pip install -e .
```

## Quick Start

### 1. Get an API Key

Choose one provider:
- [OpenAI](https://platform.openai.com/api-keys)
- [Anthropic Claude](https://console.anthropic.com/)
- [Google Gemini](https://aistudio.google.com/app/apikey)

### 2. Run Your First Test

```bash
doctai --docs README.md \
        --provider anthropic \
        --api-key your-api-key
```

That's it! doctai will:
1. Read your documentation
2. Generate test scripts using AI
3. Execute them to verify everything works

## Next Steps

- [Configure with `.doctai.yml`](guides/configuration.html) for easier usage
- [Use in GitHub Actions](github-actions.html) for automated testing
- [Explore all features](guides/features.html)

