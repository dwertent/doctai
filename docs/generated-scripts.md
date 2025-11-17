---
layout: default
title: Generated Scripts
nav_order: 6
---

# Generated Scripts
{: .no_toc }

The doc-tester saves all generated scripts to disk for inspection and debugging.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Naming Convention

Generated scripts follow this naming pattern:
```
_gen-<source-path>-<random>.<ext>
```

### Examples:
- `_gen-tests_fixtures_mock-projects_flask-api_README.md-9owq87.sh`
- `_gen-README.md-abc123.py`
- `_gen-https___example.com_docs_setup.md-xyz789.sh`

### Components:
1. **Prefix**: `_gen-` (for easy identification and gitignore)
2. **Source**: Sanitized path/URL of the documentation source
3. **Random**: 6-character random suffix (lowercase letters + digits)
4. **Extension**: `.sh` for bash, `.py` for python, etc.

## Git Integration

All generated scripts are automatically ignored by git:

```gitignore
# Generated scripts from doc-tester
_gen-*
```

This means you can inspect the scripts locally without committing them.

## Location

Scripts are saved in the current working directory where you run the command:

```bash
# Run doc-tester
doc-tester --docs README.md

# Scripts will be saved in current directory
ls _gen-*
# _gen-README.md-abc123.sh
# _gen-README.md-def456.py
```

## When Testing Documentation

When you run:
```bash
doc-tester --docs path/to/docs.md
```

The tool will:
1. ✅ Generate test scripts from the documentation
2. ✅ Save each script with the `_gen-` naming pattern
3. ✅ Execute the scripts
4. ✅ Show you where the scripts were saved
5. ✅ Keep the scripts after execution (not deleted)

## Output Example

```
================================================================================
STEP 3: Executing Test Scripts
================================================================================

============================================================
Executing bash script: _gen-README.md-abc123.sh
Saved to: /path/to/project/_gen-README.md-abc123.sh
============================================================

...

============================================================
Generated scripts saved to:
  - /path/to/project/_gen-README.md-abc123.sh
  - /path/to/project/_gen-README.md-def456.py
============================================================
```

## Benefits

1. **Debugging**: Inspect generated scripts to understand what the AI created
2. **Learning**: See how the AI interprets documentation
3. **Iteration**: Modify and re-run scripts manually if needed
4. **Troubleshooting**: Share scripts when reporting issues
5. **Testing**: Verify script quality in E2E tests

## Cleanup

To remove all generated scripts:
```bash
rm -f _gen-*
```

Or clean scripts from a specific source:
```bash
rm -f _gen-README.md-*
```

## E2E Testing

When running E2E tests, the generated scripts are also saved:

```bash
pytest tests/e2e/ -v -m requires_api

# Check generated scripts
ls _gen-*
# _gen-s_tests_fixtures_mock-projects_flask-api_README.md-xyz789.sh
# _gen-s_tests_fixtures_mock-projects_nodejs-cli_README.md-abc123.sh
```

This allows you to inspect what scripts the AI generated during testing.

