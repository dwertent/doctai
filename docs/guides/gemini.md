---
layout: default
title: Gemini Setup
parent: Guides
nav_order: 3
---

# Google Gemini Setup Guide

Quick guide for using Google Gemini with Documentation Tester.

## Getting Your API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Configuration

### Method 1: Environment Variable

```bash
export DOC_TESTER_API_KEY="your-gemini-api-key-here"
export DOC_TESTER_PROVIDER="gemini"
```

### Method 2: Command Line

```bash
doc-tester --docs README.md \
  --api-key "your-gemini-api-key" \
  --provider gemini
```

## Usage Examples

### Basic Usage

```bash
doc-tester --docs README.md \
  --api-key $DOC_TESTER_API_KEY \
  --provider gemini
```

### With Specific Model

```bash
doc-tester --docs README.md \
  --api-key $DOC_TESTER_API_KEY \
  --provider gemini \
  --model gemini-1.5-pro-latest
```

### Multiple Documents

```bash
doc-tester --docs README.md INSTALL.md \
  --api-key $DOC_TESTER_API_KEY \
  --provider gemini
```

### With Output File

```bash
doc-tester --docs README.md \
  --api-key $DOC_TESTER_API_KEY \
  --provider gemini \
  --output results.json
```

## Available Models

Gemini provides several models. The default is `gemini-1.5-pro-latest`, but you can also use:

- `gemini-1.5-pro-latest` - Latest Gemini 1.5 Pro (default)
- `gemini-1.5-flash-latest` - Faster, lighter model
- `gemini-pro` - Previous generation

Example with Flash model:

```bash
doc-tester --docs README.md \
  --api-key $DOC_TESTER_API_KEY \
  --provider gemini \
  --model gemini-1.5-flash-latest
```

## GitHub Actions Integration

To use Gemini in GitHub Actions:

1. Add your Gemini API key as a repository secret:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `GEMINI_API_KEY`
   - Value: Your Gemini API key

2. Use the workflow with Gemini provider:

```yaml
name: Test Documentation

on: [push]

jobs:
  test-docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install doc-tester
    - run: |
        doc-tester \
          --docs README.md \
          --api-key ${{ secrets.GEMINI_API_KEY }} \
          --provider gemini
```

Or use the included workflow with manual trigger:

1. Go to Actions → Test Documentation
2. Click "Run workflow"
3. Select `gemini` as the provider
4. Click "Run workflow"

## Example Script

Use the provided example script:

```bash
export GEMINI_API_KEY="your-api-key"
./examples/gemini-example.sh
```

## API Costs

Google Gemini offers competitive pricing:

- **Gemini 1.5 Pro**: 
  - Free tier: 2 requests per minute
  - Paid: ~$0.001-0.007 per 1K characters
  
- **Gemini 1.5 Flash**: 
  - Free tier: 15 requests per minute
  - Lower cost than Pro

Check the latest pricing at: https://ai.google.dev/pricing

## Troubleshooting

### "Failed to communicate with Gemini"

**Solution**: Check that:
- Your API key is correct
- You have API access enabled
- You haven't exceeded rate limits

### "Unexpected response format from Gemini API"

**Solution**: 
- Verify you're using a supported model
- Check your API key has proper permissions
- Try with the default model (`gemini-1.5-pro-latest`)

### Rate Limits

Free tier has rate limits:
- 2 requests/minute for Pro
- 15 requests/minute for Flash

**Solution**: 
- Wait and retry
- Upgrade to paid tier
- Use Flash model for testing

## Comparison with Other Providers

| Feature | OpenAI | Anthropic | Gemini |
|---------|--------|-----------|--------|
| Cost | $$$ | $$$ | $ |
| Speed | Fast | Fast | Very Fast (Flash) |
| Context | 128K | 200K | 1M+ |
| Free Tier | Limited | Limited | Yes |

Gemini is great for:
- ✅ Cost-effective testing
- ✅ Very large documentation
- ✅ Fast iteration with Flash model
- ✅ Experimentation with free tier

## Best Practices

1. **Start with Free Tier**: Test with the free tier before upgrading
2. **Use Flash for Development**: Faster and cheaper for testing
3. **Use Pro for Production**: More capable for complex documentation
4. **Monitor Usage**: Keep track of API usage to avoid surprises
5. **Cache Results**: Use `--output` to save results and avoid re-runs

## Additional Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Gemini Pricing](https://ai.google.dev/pricing)
- [API Key Management](https://aistudio.google.com/app/apikey)

---

**Happy Testing with Gemini!** 🚀

