# doctai

> **doc-t-ai**: AI-powered documentation testing

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Stop wondering if your docs work—know for certain.**

doctai automatically tests your documentation by reading it with AI, generating test scripts, and executing them. Perfect for READMEs, installation guides, tutorials, and setup instructions.

---

## 🚀 Quick Start

### 1. Install

```bash
git clone https://github.com/dwertent/doctai.git
cd doctai
pip install -e .
```

### 2. Get an API Key

Get a free API key from one of these providers:
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic (Claude)**: https://console.anthropic.com/
- **Google Gemini**: https://aistudio.google.com/app/apikey

### 3. Run

```bash
# Test the example documentation
doctai --docs examples/sample-documentation.md \
        --provider anthropic \
        --api-key your-api-key
```

That's it! doctai will read the documentation, generate test scripts, and verify everything works.

**Tip**: For regular use, create a [`.doctai.yml` config file](https://dwertent.github.io/doctai/guides/configuration.html) to avoid typing flags every time.

---

## 📖 What It Does

doctai uses AI to:

1. **Read** your documentation
2. **Understand** what needs to be installed and tested
3. **Generate** executable test scripts (bash, python, etc.)
4. **Execute** the scripts to verify everything works
5. **Report** results so you know if your docs are accurate

---

## 💡 Use Cases

- ✅ **CI/CD Integration** - Automatically test docs in your pipeline
- ✅ **Installation Guides** - Verify setup instructions work
- ✅ **API Tutorials** - Test code examples actually run
- ✅ **Quick Starts** - Ensure new users can get started
- ✅ **README Validation** - Keep your README accurate

---

## 📚 Documentation

**[View Full Documentation →](https://dwertent.github.io/doctai/)**

The documentation includes:

- 📖 [Getting Started Guide](https://dwertent.github.io/doctai/getting-started/get-started.html)
- ⚙️ [Configuration Options](https://dwertent.github.io/doctai/guides/configuration.html)
- 🔑 [API Key Setup](https://dwertent.github.io/doctai/api-key-configuration.html)
- 🎨 [Custom Instructions](https://dwertent.github.io/doctai/guides/instructions.html)
- 🤖 [AI Provider Setup](https://dwertent.github.io/doctai/guides/gemini.html) (OpenAI, Claude, Gemini)
- 🔍 [Generated Scripts](https://dwertent.github.io/doctai/generated-scripts.html)
- 🏗️ [Architecture](https://dwertent.github.io/doctai/reference/architecture.html)
- 🤝 [Contributing](https://dwertent.github.io/doctai/reference/contributing.html)

---

## 🤖 GitHub Actions

Use doctai in your CI/CD pipeline:

```yaml
name: Test Documentation

on: [push, pull_request]

jobs:
  test-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install doctai
        run: |
          pip install -e .
      
      - name: Test Documentation
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: doctai
```

**[See GitHub Actions Guide →](https://dwertent.github.io/doctai/)**

---

## 🧪 Example

Here's what doctai does with your README:

```bash
$ doctai

================================================================================
STEP 1: Fetching Documentation
================================================================================
✓ Fetched: README.md (1,245 characters)

================================================================================
STEP 2: Analyzing Documentation with AI
================================================================================
✓ Generated 3 test script(s)

================================================================================
STEP 3: Executing Test Scripts
================================================================================
✓ Script 1: Install dependencies
✓ Script 2: Run example code
✓ Script 3: Verify output

================================================================================
TEST RESULTS SUMMARY
================================================================================
Scripts passed: 3 ✓
Overall result: ✓ SUCCESS
================================================================================
```

---

## 🔧 Advanced Features

For advanced usage, see the [full documentation](https://dwertent.github.io/doctai/):

- **Multiple AI Providers** - Use OpenAI, Claude, Gemini, or custom endpoints
- **Configuration Files** - YAML/JSON config for complex setups
- **Custom Instructions** - Guide AI behavior with specific requirements
- **Multiple Sources** - Test multiple docs, URLs, or directories
- **Script Inspection** - Review generated scripts before/after execution
- **Flexible API Keys** - Use provider-specific environment variables

---

## 🤝 Contributing

Contributions welcome! See the [Contributing Guide](https://dwertent.github.io/doctai/reference/contributing.html).

---

## 📄 License

Apache-2.0 License - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

- 📚 [Documentation](https://dwertent.github.io/doctai/)
- 🐙 [GitHub](https://github.com/dwertent/doctai)
- 🐛 [Issues](https://github.com/dwertent/doctai/issues)
- 💬 [Discussions](https://github.com/dwertent/doctai/discussions)

---

**Made with ❤️ for better documentation**
