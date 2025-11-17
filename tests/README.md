# Testing Documentation

This directory contains the test suite for doctai.

## Structure

```
tests/
├── unit/                    # Unit tests (fast, no external deps)
│   ├── test_fetcher.py
│   ├── test_config.py
│   ├── test_executor.py
│   ├── test_ai_client.py
│   └── test_orchestrator.py
│
├── integration/             # Integration tests (mocked AI)
│   ├── test_config_flow.py
│   ├── test_script_generation.py
│   └── test_full_workflow.py
│
├── e2e/                     # End-to-end tests (may use real AI)
│   ├── test_sample_docs.py
│   └── test_self_test.py
│
├── fixtures/                # Test data
│   ├── sample-docs/
│   ├── configs/
│   └── ai-responses/
│
├── mocks/                   # Mock objects and responses
│   └── __init__.py
│
├── conftest.py             # Pytest configuration
└── README.md               # This file
```

## Running Tests

### All Tests

```bash
pytest
```

### Unit Tests Only

```bash
pytest tests/unit/
```

### Integration Tests

```bash
pytest tests/integration/
```

### End-to-End Tests

```bash
# Requires API key
export DOCTAI_API_KEY="your-key"
pytest tests/e2e/
```

### With Coverage

```bash
pytest --cov=doc_tester --cov-report=html
open htmlcov/index.html
```

### Specific Test

```bash
pytest tests/unit/test_fetcher.py::TestDocumentationFetcher::test_fetch_single_file
```

## Test Categories

### Unit Tests (Fast, ~30 seconds)

- Test individual modules in isolation
- Mock all external dependencies
- No API calls, no network requests
- Run on every commit

**Example:**
```bash
pytest tests/unit/ -v
```

### Integration Tests (Medium, ~2 minutes)

- Test component interactions
- Mock only AI API calls
- Real file system, real script execution
- Run on every PR

**Example:**
```bash
pytest tests/integration/ -v
```

### E2E Tests (Slower, ~5-10 minutes)

- Test complete workflows
- May use real AI (optional)
- Test actual documentation
- Run on main branch only

**Example:**
```bash
DOCTAI_API_KEY=$KEY pytest tests/e2e/ -v
```

## Writing Tests

### Test Naming Convention

```python
# File: test_<module>.py
# Class: Test<ClassName>
# Method: test_<what_it_tests>

def test_fetch_single_file():
    """Test fetching a single documentation file."""
    # Arrange
    # Act
    # Assert
```

### Using Fixtures

```python
def test_with_fixture(temp_dir, sample_doc):
    """Use pytest fixtures from conftest.py."""
    doc_file = temp_dir / "test.md"
    doc_file.write_text(sample_doc)
    # ... test code
```

### Mocking AI Responses

```python
from unittest.mock import Mock, patch

@patch('doc_tester.ai_client.requests.post')
def test_ai_client(mock_post):
    """Test AI client with mocked response."""
    mock_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "Test response"}}]
    }
    # ... test code
```

## CI/CD Integration

Tests run automatically in GitHub Actions:

- **Pull Requests:** Unit + Integration tests (fast)
- **Main Branch:** All tests including E2E
- **Weekly:** Comprehensive tests with all AI providers

## Test Coverage

Current coverage goals:

- **Overall:** >80%
- **Critical modules:** >90%
- **Fetcher:** >85%
- **Config:** >85%
- **Executor:** >80%
- **Orchestrator:** >75%

## Adding New Tests

1. Create test file in appropriate directory
2. Follow naming conventions
3. Use fixtures from conftest.py
4. Add docstrings
5. Run tests locally
6. Commit with tests

## Common Issues

### Import Errors

Make sure to install in development mode:
```bash
pip install -e .
```

### Fixture Not Found

Check that conftest.py is in the right place and pytest can find it.

### Slow Tests

Use mocks for external dependencies (AI, network).

### Flaky Tests

- Avoid timing-dependent tests
- Use deterministic test data
- Mock non-deterministic behavior

## Continuous Improvement

- Review test failures immediately
- Add tests for reported bugs
- Refactor tests as code changes
- Monitor test duration
- Keep fixtures up to date

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Goal:** Maintain high-quality, fast, and reliable tests that give us confidence in the codebase! 🎯

