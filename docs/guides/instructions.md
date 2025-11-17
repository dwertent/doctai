---
layout: default
title: Custom Instructions
parent: Guides
nav_order: 2
---

# Custom Instructions Guide

Learn how to use custom instructions to guide the AI in testing your documentation.

## Overview

While the AI is great at following documentation, sometimes you need to provide additional context or specific requirements. The `instructions` field lets you tell the AI exactly how you want the documentation tested.

## Why Use Custom Instructions?

### Without Instructions

```bash
# AI just follows the documentation as written
doctai --docs README.md --api-key $API_KEY
```

The AI will:
- Follow everything literally
- Not know about environment limitations
- Test everything equally
- May fail on environment-specific issues

### With Instructions

```yaml
# .doctai.yml
docs:
  - README.md

instructions: |
  - Skip Docker examples (not available in CI)
  - Use Python 3.10+
  - Focus on core features only
```

The AI will:
- Understand your environment constraints
- Prioritize what matters
- Adapt to your specific needs
- Be more likely to succeed

## How to Use Instructions

### Method 1: In Config File

```yaml
# .doctai.yml
docs:
  - README.md
  - docs/installation.md

instructions: |
  Test on Ubuntu 22.04 LTS.
  Use Python 3.10 or higher.
  Skip examples requiring external services.
```

### Method 2: Command Line

```bash
doctai --docs README.md \
  --instructions "Test installation on Ubuntu. Skip Docker examples." \
  --api-key $API_KEY
```

### Method 3: Combination

Config provides defaults, CLI overrides:

```yaml
# .doctai.yml
instructions: "Default testing guidelines"
```

```bash
# Override with specific instructions
doctai --instructions "Special test for this run" --api-key $API_KEY
```

## Instruction Types

### 1. Environment Constraints

Tell the AI about your testing environment:

```yaml
instructions: |
  Testing environment:
  - Ubuntu 22.04 LTS
  - Python 3.10
  - No Docker available
  - No database server
  - Limited internet access (internal only)
```

### 2. Focus Areas

Direct the AI's attention:

```yaml
instructions: |
  Focus areas:
  - Test installation guide thoroughly
  - Run all "Getting Started" examples
  - Skip advanced configuration
  - Skip performance benchmarking section
```

### 3. Substitutions

Provide test values:

```yaml
instructions: |
  Substitutions:
  - Use test API endpoint: https://api.test.example.com
  - Use dummy API key: test-key-12345
  - Replace database URL with: sqlite:///test.db
  - Use test user: testuser@example.com
```

### 4. Specific Flows

Guide through particular scenarios:

```yaml
instructions: |
  For document A (installation.md):
  - Test the "Quick Install" section first
  - Then test "Manual Installation"
  - Skip "Docker Installation"
  
  For document B (api.md):
  - Focus on authentication examples
  - Test all CRUD operations
  - Skip webhooks section
```

### 5. Error Handling

Specify how to handle issues:

```yaml
instructions: |
  Error handling:
  - If installation fails, try alternative method
  - Continue testing even if one example fails
  - Document all errors but don't stop execution
  - Use fallback values if configuration fails
```

## Real-World Examples

### Example 1: CI/CD Environment

```yaml
docs:
  - README.md
  - INSTALL.md

instructions: |
  CI Environment Constraints:
  - Running in GitHub Actions Ubuntu runner
  - No GUI available (headless)
  - No Docker daemon available
  - Limited to 6GB RAM
  - No external network access except to GitHub
  
  Testing Requirements:
  - Use pip instead of conda
  - Skip GUI examples
  - Use in-memory database for tests
  - Mock external API calls
```

### Example 2: Specific Version Testing

```yaml
docs:
  - docs/installation.md

instructions: |
  Version Testing for v2.0:
  - Install version 2.0.0 specifically (not latest)
  - Test compatibility with Python 3.8, 3.9, and 3.10
  - Verify all examples work with this version
  - Check that deprecated features show warnings
```

### Example 3: Platform-Specific

```yaml
docs:
  - README.md

instructions: |
  Windows Platform Testing:
  - Use Windows-style paths (C:\\ not /)
  - Use PowerShell commands, not bash
  - Install using pip (WSL not available)
  - Test with Python installed from python.org
```

### Example 4: Feature-Focused

```yaml
docs:
  - README.md
  - docs/api.md
  - docs/tutorial.md

instructions: |
  Feature: Testing Authentication Flow
  
  In README.md:
  - Only test the "Authentication" section
  
  In docs/api.md:
  - Test all authentication endpoints (/login, /logout, /token)
  - Use test credentials: user=testuser, pass=testpass123
  
  In docs/tutorial.md:
  - Follow the "User Authentication Tutorial"
  - Skip other tutorials for now
```

### Example 5: Multi-Document Strategy

```yaml
docs:
  - docs/quickstart.md
  - docs/advanced.md
  - docs/api-reference.md

instructions: |
  Testing Strategy:
  
  Phase 1 - Quickstart (docs/quickstart.md):
  - Test every single step
  - This is our primary user flow
  - Must work 100%
  
  Phase 2 - Advanced (docs/advanced.md):
  - Test key examples only
  - Focus on sections 3.1 and 3.2
  - Skip optimization tips (section 4)
  
  Phase 3 - API Reference (docs/api-reference.md):
  - Test one example from each API category
  - Don't test every endpoint
  - Focus on common use cases
```

## Tips for Writing Good Instructions

### ✅ DO

1. **Be Specific**
   ```yaml
   # Good
   instructions: "Use Python 3.10.5. Test on Ubuntu 22.04 LTS."
   
   # Bad
   instructions: "Use recent Python. Test on Linux."
   ```

2. **Provide Context**
   ```yaml
   # Good
   instructions: |
     We're in CI environment with no Docker.
     Use pip instead.
   
   # Bad
   instructions: "No Docker"
   ```

3. **Prioritize**
   ```yaml
   # Good
   instructions: |
     Priority 1: Test installation (critical)
     Priority 2: Test basic examples
     Priority 3: Advanced features (if time permits)
   ```

4. **Give Alternatives**
   ```yaml
   # Good
   instructions: |
     If PostgreSQL not available, use SQLite.
     If Redis not available, use in-memory cache.
   ```

### ❌ DON'T

1. **Don't Be Vague**
   ```yaml
   # Bad
   instructions: "Test stuff carefully"
   ```

2. **Don't Contradict Documentation**
   ```yaml
   # Bad (if docs say Python 3.8+)
   instructions: "Use Python 2.7"
   ```

3. **Don't Be Too Restrictive**
   ```yaml
   # Bad
   instructions: "Only test line 42 of README.md and nothing else"
   ```

4. **Don't Include Secrets**
   ```yaml
   # DANGEROUS!
   instructions: "Use API key: sk-real-api-key-12345"
   ```

## Formatting Options

### Simple String

```yaml
instructions: "Test on Ubuntu 22.04. Use Python 3.10+. Skip Docker."
```

### Multi-Line String

```yaml
instructions: |
  Environment: Ubuntu 22.04
  Python: 3.10+
  Skip: Docker examples
```

### List Format

```yaml
instructions:
  - Test on Ubuntu 22.04 LTS
  - Use Python 3.10 or higher
  - Skip all Docker examples
  - Focus on core functionality
```

## CLI vs Config File

### Config File (Recommended)

**Pros:**
- ✅ Consistent across runs
- ✅ Documented in repository
- ✅ Easy to maintain
- ✅ Team can see what's tested

**Example:**
```yaml
# .doctai.yml
instructions: "Standard testing guidelines..."
```

### Command Line

**Pros:**
- ✅ Quick one-off tests
- ✅ Override config temporarily
- ✅ Good for experimentation

**Example:**
```bash
doctai --instructions "Special test case" --api-key $KEY
```

## GitHub Actions Integration

In your workflow, instructions from config file are automatically used:

```yaml
# .github/workflows/test-docs.yml
- name: Test Documentation
  run: doctai --api-key ${{ secrets.OPENAI_API_KEY }}
```

The workflow will use instructions from your `.doctai.yml` automatically!

## Advanced: Dynamic Instructions

Generate instructions programmatically:

```bash
#!/bin/bash

# Detect environment
if [ "$CI" = "true" ]; then
  INSTRUCTIONS="CI environment. No Docker. Use pip only."
else
  INSTRUCTIONS="Local environment. Full features available."
fi

doctai --instructions "$INSTRUCTIONS" --api-key $API_KEY
```

## Common Use Cases

### Skip Sections

```yaml
instructions: |
  Skip the following sections:
  - Docker Installation (section 2.3)
  - Kubernetes Deployment (section 5)
  - Performance Benchmarking (appendix B)
```

### Test Specific Flow

```yaml
instructions: |
  Follow this specific flow:
  1. Install dependencies (section 1)
  2. Configure for development (section 2.1, NOT 2.2)
  3. Run the "Hello World" example (section 3)
  4. Stop here (don't continue to section 4)
```

### Platform Adaptation

```yaml
instructions: |
  Platform: macOS
  - Use 'brew' package manager
  - Python installed via 'brew install python@3.10'
  - Use zsh shell syntax
```

### Minimal Testing

```yaml
instructions: |
  Minimal smoke test only:
  - Verify installation works
  - Run one basic example
  - Don't test advanced features
  - Quick validation only
```

## Troubleshooting

### Instructions Not Working?

1. **Check formatting:**
   ```yaml
   # Make sure indentation is correct
   instructions: |
     Line 1
     Line 2
   ```

2. **Verify CLI override:**
   ```bash
   # CLI always wins
   doctai --instructions "CLI overrides config"
   ```

3. **Test verbosity:**
   ```bash
   # See what AI receives
   doctai --docs README.md --instructions "test" --api-key $KEY
   ```

### AI Ignoring Instructions?

Make instructions more explicit:

```yaml
# Weak
instructions: "Maybe skip Docker"

# Strong
instructions: |
  IMPORTANT: Do NOT attempt Docker installation.
  Skip all Docker-related sections entirely.
```

## Summary

Custom instructions let you:
- ✅ Guide AI behavior
- ✅ Handle environment constraints
- ✅ Focus on what matters
- ✅ Improve test success rate
- ✅ Document testing strategy

**Quick Start:**

```yaml
# .doctai.yml
docs:
  - README.md

instructions: |
  - Test on your actual environment
  - Provide clear constraints
  - Guide the AI to success!
```

```bash
doctai --api-key $API_KEY
```

For more examples, see [examples/config-with-instructions.yml](examples/config-with-instructions.yml).

---

**Ready to guide your documentation testing?** Add instructions to your config file and watch your tests become more reliable! 🎯

