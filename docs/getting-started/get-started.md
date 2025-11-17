---
layout: default
title: Get Started in 3 Steps
parent: Getting Started
nav_order: 3
---

# Get Started in 3 Steps

The fastest way to start using doctai.

## Step 1: Install (2 minutes)

Run the automated setup script:

```bash
cd /Users/dwertent/kaleido/temp/test-docs
./test_setup.sh
```

This will:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Run tests to verify everything works

## Step 2: Configure (30 seconds)

Get an API key and set it:

### For OpenAI:
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Run:
```bash
export DOCTAI_API_KEY="sk-your-key-here"
```

### For Anthropic:
1. Visit https://console.anthropic.com/
2. Create an API key
3. Run:
```bash
export DOCTAI_API_KEY="sk-ant-your-key-here"
export DOCTAI_PROVIDER="anthropic"
```

### For Google Gemini:
1. Visit https://aistudio.google.com/app/apikey
2. Create an API key
3. Run:
```bash
export DOCTAI_API_KEY="your-gemini-key-here"
export DOCTAI_PROVIDER="gemini"
```

## Step 3: Test (1 minute)

Activate the virtual environment and test:

```bash
source venv/bin/activate
doctai --docs examples/sample-documentation.md --api-key $DOCTAI_API_KEY
```

You should see:
```
STEP 1: Fetching Documentation
STEP 2: Analyzing Documentation with AI
STEP 3: Executing Test Scripts
✓ SUCCESS
```

## What Just Happened?

1. 📄 **Fetched**: Read the example documentation
2. 🤖 **Analyzed**: AI understood the setup instructions
3. 🛠️ **Generated**: AI created test scripts
4. ▶️ **Executed**: Ran the scripts automatically
5. ✅ **Verified**: Confirmed everything works!

## Next Steps

### Test Your Own Documentation

```bash
doctai --docs YOUR_README.md --api-key $DOCTAI_API_KEY
```

### Test Multiple Files

```bash
doctai --docs README.md docs/setup.md docs/install.md --api-key $DOCTAI_API_KEY
```

### Test Documentation from URL

```bash
doctai --docs https://raw.githubusercontent.com/user/repo/main/README.md --api-key $DOCTAI_API_KEY
```

### Save Results

```bash
doctai --docs README.md --api-key $DOCTAI_API_KEY --output results.json
```

### Run in CI/CD

Copy `.github/workflows/test-docs.yml` to your repo and add your API key as a GitHub secret.

## Troubleshooting

### "command not found: doctai"

Activate the virtual environment:
```bash
source venv/bin/activate
```

### "API key is required"

Set your API key:
```bash
export DOCTAI_API_KEY="your-key-here"
```

### "No test scripts were generated"

Your documentation might need more explicit instructions. The AI looks for:
- Installation commands
- Setup instructions
- Code examples
- Verification steps

## Learn More

- **Quick Tutorial**: [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation**: [README.md](README.md)
- **Installation Guide**: [INSTALL.md](INSTALL.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Common Use Cases

### 1. Test Installation Instructions

```bash
doctai --docs docs/installation.md --api-key $DOCTAI_API_KEY
```

### 2. Test Getting Started Guide

```bash
doctai --docs docs/getting-started.md --api-key $DOCTAI_API_KEY
```

### 3. Test Tutorial

```bash
doctai --docs docs/tutorial.md --api-key $DOCTAI_API_KEY
```

### 4. Test All Documentation

```bash
doctai --docs docs/ --api-key $DOCTAI_API_KEY
```

## Tips for Better Results

1. **Be Explicit**: Clear, step-by-step instructions work best
2. **Include Commands**: Show exact commands to run
3. **Add Examples**: Code examples help AI understand
4. **Specify Prerequisites**: List what's needed upfront
5. **Include Verification**: Add steps to verify success

## Example Documentation Format

The AI works best with documentation like this:

```markdown
# Project Setup

## Prerequisites
- Python 3.8+
- pip

## Installation

1. Install dependencies:
   ```bash
   pip install requests
   ```

2. Create main script:
   ```bash
   echo "print('Hello')" > app.py
   ```

3. Run the script:
   ```bash
   python app.py
   ```

## Verification
You should see "Hello" printed to the console.
```

## Support

- 🐛 **Bugs**: Open an issue on GitHub
- 💡 **Ideas**: Start a discussion
- 📧 **Questions**: Check existing discussions

---

**Happy Testing!** 🚀

Now your documentation will always work!

