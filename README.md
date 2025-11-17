# Documentation Tester

**AI-powered documentation testing tool** that automatically verifies your documentation by reading it, understanding it through AI, generating test scripts, and executing them.

## 🚀 Overview

Documentation Tester solves a common problem: **outdated or broken documentation**. It uses AI to:

1. **Read** your documentation (setup guides, tutorials, installation instructions)
2. **Understand** what needs to be done through AI analysis
3. **Generate** executable test scripts (bash, python, etc.)
4. **Execute** those scripts to verify everything works
5. **Report** results so you know if your docs are accurate

Perfect for:
- ✅ CI/CD pipelines (via GitHub Actions)
- ✅ Regular documentation validation
- ✅ Testing installation guides
- ✅ Verifying tutorials and examples
- ✅ Ensuring setup instructions work

## 📋 Features

- **Multiple AI Providers**: OpenAI, Anthropic Claude, Google Gemini, or custom endpoints
- **Flexible Sources**: Read from local files, directories, or URLs
- **Configuration Files**: YAML/JSON config files for easy project setup
- **Smart Script Generation**: AI generates appropriate bash/python/other scripts
- **Safe Execution**: Isolated execution with configurable timeouts
- **GitHub Actions Integration**: Easy CI/CD integration with auto-config loading
- **Custom Instructions**: Guide AI behavior with specific requirements
- **Detailed Reporting**: JSON output for programmatic processing

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
git clone https://github.com/yourusername/doc-tester.git
cd doc-tester

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install doc-tester
pip install -e .
```

## 🔧 Configuration

### API Keys

Get an API key from one of these providers:

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google Gemini**: https://aistudio.google.com/app/apikey

Set your API key:

```bash
export DOC_TESTER_API_KEY="your-api-key-here"
```

Or pass it via command line with `--api-key`.

## 📖 Usage

### Basic Usage

Test a single documentation file:

```bash
doc-tester --docs README.md --api-key $DOC_TESTER_API_KEY
```

Test multiple documentation files:

```bash
doc-tester --docs README.md docs/setup.md docs/tutorial.md --api-key $DOC_TESTER_API_KEY
```

Test documentation from a URL:

```bash
doc-tester --docs https://example.com/docs/installation.md --api-key $DOC_TESTER_API_KEY
```

### Using Configuration Files

Create a `.doc-tester.yml` file in your project root:

```yaml
docs:
  - README.md
  - docs/installation.md
  - docs/quickstart.md

provider: openai
model: gpt-4o

stop_on_failure: false
max_iterations: 3
timeout: 120

instructions: |
  Test on Ubuntu 22.04
  Use Python 3.11
  Skip Docker examples
```

Then simply run:

```bash
doc-tester --api-key $DOC_TESTER_API_KEY
```

### Specify AI Provider

```bash
# Use OpenAI (default)
doc-tester --docs README.md --provider openai --api-key $OPENAI_API_KEY

# Use Anthropic Claude
doc-tester --docs README.md --provider anthropic --api-key $ANTHROPIC_API_KEY

# Use Google Gemini
doc-tester --docs README.md --provider gemini --api-key $GEMINI_API_KEY
```

### API Key Configuration

By default, the tool reads the API key from the `DOC_TESTER_API_KEY` environment variable. However, you can configure it to use provider-specific environment variables or any custom variable name.

**Method 1: In config file** (recommended):
```yaml
# .doc-tester.yml
provider: anthropic
api_key_env_var: ANTHROPIC_API_KEY  # Use provider-specific env var
```

Then just set the provider's environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
doc-tester
```

**Method 2: Environment variable override**:
```bash
export OPENAI_API_KEY="sk-..."
export DOC_TESTER_API_KEY_ENV_VAR=OPENAI_API_KEY
doc-tester --docs README.md
```

This is particularly useful when working with multiple projects that use different AI providers. See the [API Key Configuration Guide](docs/api-key-configuration.md) for more details.

### Custom Instructions

Add custom instructions to guide AI behavior:

```bash
doc-tester --docs README.md \
  --instructions "Test on macOS only, skip database setup" \
  --api-key $DOC_TESTER_API_KEY
```

Or in your config file:

```yaml
docs:
  - README.md

instructions: |
  Test on macOS only
  Skip database setup
  Use Node.js 18
```

### Command-Line Options

```
doc-tester [OPTIONS]

Options:
  --docs TEXT              Documentation files or URLs (can specify multiple)
  --config TEXT           Path to config file (default: .doc-tester.yml)
  --provider TEXT         AI provider: openai, anthropic, gemini, custom
  --model TEXT            AI model to use
  --api-key TEXT          AI API key
  --api-url TEXT          Custom API endpoint URL
  --work-dir TEXT         Working directory for script execution
  --stop-on-failure       Stop testing if any script fails
  --max-iterations INT    Maximum AI interaction iterations (default: 3)
  --timeout INT           Script execution timeout in seconds (default: 120)
  --instructions TEXT     Custom instructions for AI
  --output TEXT           Output file for results (JSON)
  --quiet                 Suppress verbose output
  --help                  Show this message and exit
```

## 🤖 GitHub Actions Integration

Create `.github/workflows/test-docs.yml`:

```yaml
name: Test Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  test-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install doc-tester
        run: |
          pip install -r requirements.txt
          pip install -e .
      
      - name: Test Documentation
        env:
          DOC_TESTER_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          doc-tester --provider openai --api-key $DOC_TESTER_API_KEY
```

Add your API key as a secret in GitHub:
- Go to repository Settings → Secrets → Actions
- Add secret: `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`)

## 🧪 Testing

Documentation Tester includes comprehensive tests:

```bash
# Run all tests
./run_tests.sh all

# Run fast tests (unit + integration)
./run_tests.sh fast

# Run with coverage
./run_tests.sh coverage
```

For detailed testing information, see [TESTING.md](TESTING.md) or [HOW_TO_RUN_TESTS.md](HOW_TO_RUN_TESTS.md).

## 📚 Documentation

### Main Documentation
- **README.md** (this file) - Quick start and usage
- **TESTING_QUICK_START.md** - Testing guide for contributors
- **DOCS_SETUP.md** - Set up GitHub Pages documentation site

### Complete Documentation Site
Full documentation is available in the `docs/` directory:
- **Getting Started**: Installation, quick start, and tutorials
- **Guides**: Configuration, AI provider setup, custom instructions
- **Reference**: Architecture, API reference, contributing guide
- **Examples**: Sample configurations and use cases

To publish as GitHub Pages:
1. See [DOCS_SETUP.md](DOCS_SETUP.md) for setup instructions
2. Documentation will be available at `https://yourusername.github.io/doc-tester/`

## 💡 Example Configurations

### Basic Configuration

```yaml
# .doc-tester.yml
docs:
  - README.md
provider: openai
```

### Advanced Configuration

```yaml
# .doc-tester.yml
docs:
  - README.md
  - docs/installation.md
  - docs/quickstart.md
  - https://example.com/docs/api.md

provider: openai
model: gpt-4o

work_dir: ./test-workspace
stop_on_failure: false
max_iterations: 5
timeout: 300

instructions: |
  Test on Ubuntu 22.04 LTS
  Use Python 3.11
  Skip Docker-related examples
  Verify all API endpoints
```

## 🔧 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Make sure package is installed
pip install -e .
```

**API Key Not Found**
```bash
# Set environment variable
export DOC_TESTER_API_KEY="your-key"

# Or pass via command line
doc-tester --api-key your-key --docs README.md
```

**Scripts Timing Out**
```bash
# Increase timeout
doc-tester --docs README.md --timeout 300
```

**Virtual Environment Issues**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run tests: `./run_tests.sh fast`
6. Submit a pull request

See [docs/reference/contributing.md](docs/reference/contributing.md) for detailed guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🔗 Links

- [GitHub Repository](https://github.com/yourusername/doc-tester)
- [Issue Tracker](https://github.com/yourusername/doc-tester/issues)
- [Documentation](https://yourusername.github.io/doc-tester/) (if GitHub Pages is set up)

## ⚠️ Notes

- Test scripts run in isolated directories but have system access
- Review generated scripts in verbose mode for security
- Some documentation may require specific system dependencies
- Ensure you have a valid API key for your chosen AI provider

---

**Made with ❤️ for better documentation**
