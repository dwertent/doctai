# E2E Tests

## What These Tests Do

E2E tests validate that the AI generates **high-quality, complete scripts** from documentation. They use mock project documentation and compare AI-generated scripts against known-correct "golden" scripts.

## Quick Start

### Run the Tests 

```bash
# Set your API key
export DOCTAI_API_KEY="your-api-key"

# Run quality validation tests
pytest tests/e2e/ -v -m requires_api
```

### Run Specific Test
```bash
pytest tests/e2e/test_ai_quality.py::TestAIScriptQuality::test_flask_api_script_quality -v
```

## How It Works

1. **Mock Projects** - Fictional projects with documentation (Flask API, Node.js CLI, etc.)
2. **Golden Scripts** - Pre-written correct scripts for each project
3. **AI Generates** - Tool creates scripts from mock documentation
4. **AI Validates** - Compares generated vs golden scripts
5. **Test Asserts** - Ensures generated scripts are complete and adequate

## Mock Projects

We test with 3 realistic mock projects:

| Project | Type | What It Tests |
|---------|------|---------------|
| **flask-api** | Python web API | Installation, server setup, API testing |
| **nodejs-cli** | Node.js CLI tool | npm setup, executable creation, functionality |
| **python-data-analysis** | Data science | Library install, data processing, verification |

## Test Structure

```
tests/fixtures/mock-projects/
├── flask-api/
│   ├── README.md           # Mock documentation
│   └── golden_script.sh    # Known-correct script
├── nodejs-cli/
│   ├── README.md
│   └── golden_script.sh
└── python-data-analysis/
    ├── README.md
    └── golden_script.sh
```

## Why This Approach?

Traditional E2E tests just check if code runs. These tests validate **quality**:

- ✅ Generated scripts include all critical steps
- ✅ No missing dependencies
- ✅ Proper verification/testing included
- ✅ Scripts actually work


## Adding New Mock Projects

1. Create directory: `tests/fixtures/mock-projects/my-project/`
2. Add `README.md` with realistic documentation
3. Add `golden_script.sh` with correct implementation
4. Add test in `test_ai_quality.py`

## Troubleshooting

**"Golden script missing"**
```bash
chmod +x tests/fixtures/mock-projects/*/golden_script.sh
```

**"No script was generated"**
- Check API key is valid
- Verify doctai can access mock README

**"AI comparison failed"**
- Check network connectivity
- Verify API provider is available

---

**These tests ensure AI generates quality scripts, not just any scripts!** 🎯
