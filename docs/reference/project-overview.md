---
layout: default
title: Project Overview
parent: Reference
nav_order: 3
---

# doctai - Project Summary

## Overview

**doctai** is an AI-powered tool that automatically tests documentation by reading it, understanding it through AI, generating executable test scripts, and running them to verify accuracy.

## Problem Statement

Documentation becomes outdated quickly. Installation guides, setup instructions, and tutorials often contain errors or become obsolete as projects evolve. Manually testing documentation is time-consuming and often neglected.

## Solution

An automated system that:
1. **Reads** documentation from files, directories, or URLs
2. **Understands** instructions through AI analysis
3. **Generates** executable scripts (bash, python, etc.)
4. **Executes** those scripts safely
5. **Reports** results with clear pass/fail status

## Key Features

### ✅ AI-Powered Analysis
- Uses OpenAI, Anthropic Claude, or custom AI endpoints
- Understands natural language documentation
- Generates appropriate test scripts

### ✅ Flexible Input
- Local files (Markdown, text, RST, etc.)
- Directories (recursive search)
- URLs (direct HTTP/HTTPS)
- Multiple sources simultaneously

### ✅ Safe Execution
- Isolated temporary directories
- Configurable timeouts
- Captured stdout/stderr
- Multiple script types (bash, python, etc.)

### ✅ CI/CD Integration
- Ready-to-use GitHub Actions workflow
- JSON output for programmatic processing
- Exit codes for pipeline integration

### ✅ Multiple AI Providers
- OpenAI (GPT-4, etc.)
- Anthropic (Claude, etc.)
- Google Gemini (Gemini 1.5 Pro, etc.)
- Custom OpenAI-compatible endpoints

## Project Structure

```
doctai/
├── doc_tester/              # Core package
│   ├── __init__.py          # Package initialization
│   ├── fetcher.py           # Documentation retrieval
│   ├── ai_client.py         # AI provider interface
│   ├── executor.py          # Script execution engine
│   ├── orchestrator.py      # Workflow coordination
│   └── cli.py               # Command-line interface
│
├── examples/                # Example files
│   ├── sample-documentation.md
│   └── test-example.sh
│
├── .github/workflows/       # CI/CD configurations
│   └── test-docs.yml
│
├── Documentation Files
│   ├── README.md            # Main documentation
│   ├── QUICKSTART.md        # Quick start guide
│   ├── INSTALL.md           # Installation guide
│   ├── ARCHITECTURE.md      # Architecture details
│   ├── CONTRIBUTING.md      # Contribution guide
│   └── PROJECT_SUMMARY.md   # This file
│
├── Configuration Files
│   ├── requirements.txt     # Python dependencies
│   ├── setup.py             # Package setup
│   ├── .gitignore           # Git ignore rules
│   └── LICENSE              # MIT License
│
└── Test Scripts
    ├── test_installation.py # Installation verification
    └── test_setup.sh        # Complete setup script
```

## Components

### 1. Fetcher (`fetcher.py`)
- Retrieves documentation from multiple sources
- Supports files, directories, and URLs
- Handles various documentation formats

### 2. AI Client (`ai_client.py`)
- Interfaces with AI providers
- Manages conversation history
- Handles API requests/responses
- Provider-agnostic design

### 3. Executor (`executor.py`)
- Executes generated scripts safely
- Manages temporary environments
- Captures output and errors
- Supports multiple script types

### 4. Orchestrator (`orchestrator.py`)
- Coordinates the entire workflow
- Manages AI conversation
- Extracts scripts from AI responses
- Collects and formats results

### 5. CLI (`cli.py`)
- User-friendly command-line interface
- Environment variable support
- Comprehensive options
- Help and documentation

## Workflow

```
┌──────────────────────────────────────────────────────┐
│ 1. INPUT: User provides documentation sources        │
│    - Files, directories, or URLs                     │
└─────────────────┬────────────────────────────────────┘
                  ▼
┌──────────────────────────────────────────────────────┐
│ 2. FETCH: DocumentationFetcher retrieves content     │
│    - Reads files                                     │
│    - Downloads from URLs                             │
│    - Searches directories                            │
└─────────────────┬────────────────────────────────────┘
                  ▼
┌──────────────────────────────────────────────────────┐
│ 3. ANALYZE: AI analyzes documentation                │
│    - Understands instructions                        │
│    - Identifies setup steps                          │
│    - Determines prerequisites                        │
└─────────────────┬────────────────────────────────────┘
                  ▼
┌──────────────────────────────────────────────────────┐
│ 4. GENERATE: AI creates test scripts                 │
│    - Bash scripts for installation                   │
│    - Python scripts for testing                      │
│    - Other languages as needed                       │
└─────────────────┬────────────────────────────────────┘
                  ▼
┌──────────────────────────────────────────────────────┐
│ 5. EXECUTE: ScriptExecutor runs scripts              │
│    - Creates isolated environment                    │
│    - Runs with timeout protection                    │
│    - Captures all output                             │
└─────────────────┬────────────────────────────────────┘
                  ▼
┌──────────────────────────────────────────────────────┐
│ 6. REPORT: Results are collected and displayed       │
│    - Pass/fail status                                │
│    - Detailed output                                 │
│    - JSON export option                              │
└──────────────────────────────────────────────────────┘
```

## Usage Examples

### Basic Usage
```bash
doctai --docs README.md --api-key $OPENAI_API_KEY
```

### Multiple Sources
```bash
doctai --docs README.md docs/setup.md --api-key $API_KEY
```

### From URL
```bash
doctai --docs https://example.com/docs.md --api-key $API_KEY
```

### With Output
```bash
doctai --docs README.md --api-key $API_KEY --output results.json
```

### In GitHub Actions
```yaml
- run: doctai --docs README.md --api-key ${{ secrets.OPENAI_API_KEY }}
```

## Technical Specifications

### Language
- Python 3.8+

### Dependencies
- `requests` - HTTP client

### Supported AI Providers
- OpenAI API
- Anthropic API
- Google Gemini API
- Any OpenAI-compatible API

### Supported Script Types
- Bash/Shell
- Python
- Extensible to other languages

### Output Formats
- Console (colored, formatted)
- JSON (for programmatic use)

## Installation

### Quick Install
```bash
git clone https://github.com/dwertent/doctai.git
cd doctai
./test_setup.sh
```

### Manual Install
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Testing

### Verify Installation
```bash
python test_installation.py
```

### Test with Example
```bash
export DOCTAI_API_KEY="your-key"
doctai --docs examples/sample-documentation.md --api-key $DOCTAI_API_KEY
```

## GitHub Actions Integration

The project includes a ready-to-use GitHub Actions workflow that:
- Runs on push, pull requests, and weekly schedule
- Tests documentation automatically
- Supports multiple AI providers
- Provides detailed results
- Comments on pull requests

## Future Enhancements

### Short Term
- Add comprehensive unit tests
- Improve error handling
- Add retry logic for AI calls

### Medium Term
- Docker/container support
- Parallel script execution
- Result caching
- Web UI for results

### Long Term
- Plugin system
- Metrics and analytics
- Multi-language support
- Distributed execution

## Use Cases

1. **Continuous Integration**
   - Automatically test docs on every commit
   - Catch outdated instructions early
   - Maintain documentation quality

2. **Regular Validation**
   - Weekly/monthly doc verification
   - Ensure setup guides work
   - Validate installation instructions

3. **Pre-release Testing**
   - Verify docs before releases
   - Test migration guides
   - Validate upgrade procedures

4. **Documentation Development**
   - Test docs as you write them
   - Immediate feedback
   - Iterate quickly

## Benefits

- **Time Saving**: Automate manual testing
- **Quality**: Catch errors before users do
- **Confidence**: Know your docs work
- **Maintenance**: Keep docs up-to-date
- **Developer Experience**: Better onboarding

## Limitations

- **AI Accuracy**: Depends on AI understanding
- **Cost**: API calls have costs
- **Complexity**: Complex scenarios may fail
- **Environment**: Limited to script execution environment

## Security Considerations

- API keys stored as secrets
- Isolated script execution
- Timeout protection
- No arbitrary code injection

## Performance

- **Fetch**: Fast for local files, depends on network for URLs
- **AI Analysis**: 5-30 seconds per request
- **Execution**: Depends on script complexity
- **Total**: Usually 1-5 minutes per documentation set

## Cost Estimation

- **OpenAI GPT-4**: ~$0.03-0.15 per documentation test
- **Anthropic Claude**: ~$0.03-0.15 per documentation test
- Lower for simpler documentation
- Batch processing reduces costs

## Getting Started

1. **Read**: [QUICKSTART.md](QUICKSTART.md)
2. **Install**: [INSTALL.md](INSTALL.md)
3. **Learn**: [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Contribute**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Support

- **GitHub Issues**: Bug reports, feature requests
- **Discussions**: Questions, ideas, community
- **Documentation**: Comprehensive guides included

## License

MIT License - Free for personal and commercial use

## Credits

- Built with Python
- Powered by AI (OpenAI, Anthropic)
- Inspired by the need for accurate documentation

---

**doctai** - Because documentation should always work! 🚀

Version: 0.1.0
Last Updated: 2025-11-17

