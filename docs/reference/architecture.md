---
layout: default
title: Architecture
parent: Reference
nav_order: 1
---

# Architecture

This document describes the architecture of the doctai.

## Overview

doctai is a Python-based tool that uses AI to automatically test documentation by generating and executing test scripts.

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  (CLI, GitHub Actions, Direct Python Import)                 │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                      Orchestrator                            │
│  (doc_tester.orchestrator.DocumentationTester)               │
│  - Manages workflow                                          │
│  - Coordinates components                                    │
└──┬────────────────┬────────────────┬────────────────────────┘
   │                │                │
   ▼                ▼                ▼
┌──────────┐  ┌──────────┐  ┌──────────────┐
│ Fetcher  │  │AI Client │  │  Executor    │
│          │  │          │  │              │
│ - Files  │  │ - OpenAI │  │ - Bash       │
│ - URLs   │  │ - Claude │  │ - Python     │
│ - Dirs   │  │ - Custom │  │ - Safety     │
└──────────┘  └──────────┘  └──────────────┘
```

## Components

### 1. CLI (`doc_tester/cli.py`)

**Purpose**: Command-line interface for users

**Responsibilities**:
- Parse command-line arguments
- Validate configuration
- Initialize and run the orchestrator
- Output results

**Key Functions**:
- `main()`: Entry point for the CLI

### 2. Orchestrator (`doc_tester/orchestrator.py`)

**Purpose**: Main workflow coordinator

**Responsibilities**:
- Coordinate all components
- Manage the testing workflow
- Handle errors and reporting
- Control the AI conversation flow

**Key Classes**:
- `DocumentationTester`: Main orchestrator class

**Workflow**:
1. Fetch documentation
2. Send to AI for analysis
3. Extract generated scripts
4. Execute scripts
5. Collect and report results

### 3. Fetcher (`doc_tester/fetcher.py`)

**Purpose**: Retrieve documentation from various sources

**Responsibilities**:
- Read local files
- Read directories (recursive)
- Fetch from URLs
- Support multiple documentation formats

**Key Classes**:
- `DocumentationFetcher`: Handles all fetching operations

**Supported Sources**:
- Local files (`.md`, `.txt`, `.rst`, `.adoc`)
- Directories (recursive search)
- HTTP/HTTPS URLs

### 4. AI Client (`doc_tester/ai_client.py`)

**Purpose**: Communicate with AI providers

**Responsibilities**:
- Handle different AI APIs
- Manage conversation history
- Format requests/responses
- Error handling and retries

**Key Classes**:
- `AIClient`: Generic AI client
- `AIProvider`: Enum of supported providers

**Supported Providers**:
- OpenAI (GPT-4, etc.)
- Anthropic (Claude, etc.)
- Custom (OpenAI-compatible APIs)

**API Handling**:
- OpenAI format: `/v1/chat/completions`
- Anthropic format: `/v1/messages`
- Custom: Configurable endpoint

### 5. Executor (`doc_tester/executor.py`)

**Purpose**: Safely execute generated scripts

**Responsibilities**:
- Create isolated execution environment
- Execute scripts with timeouts
- Capture stdout/stderr
- Clean up resources

**Key Classes**:
- `ScriptExecutor`: Handles script execution

**Features**:
- Temporary working directories
- Configurable timeouts
- Environment variable support
- Multiple script types (bash, python, etc.)

## Data Flow

### 1. Documentation Collection

```
User Input (paths/URLs)
    ↓
DocumentationFetcher
    ↓
Dict[source, content]
```

### 2. AI Analysis

```
Documentation Content
    ↓
AIClient.send_message()
    ↓
AI Response (with code blocks)
    ↓
Script Extraction (regex)
    ↓
Dict[script_name, {content, type}]
```

### 3. Script Execution

```
Scripts
    ↓
ScriptExecutor.execute_multiple_scripts()
    ↓
For each script:
  - Write to temp file
  - Execute with timeout
  - Capture output
    ↓
Dict[script_name, (success, stdout, stderr)]
```

### 4. Results

```
Execution Results
    ↓
Orchestrator
    ↓
JSON Output / Console Display
```

## Configuration

### Environment Variables

- `DOCTAI_API_KEY`: AI API key
- `DOCTAI_API_URL`: Custom API endpoint
- `DOCTAI_PROVIDER`: AI provider name
- `DOCTAI_MODEL`: Model name

### Command-Line Options

See `cli.py` for full list of options.

## Extension Points

### Adding New AI Providers

1. Add provider to `AIProvider` enum in `ai_client.py`
2. Implement `_send_<provider>_message()` method
3. Add default URL and model
4. Update documentation

### Adding New Script Types

1. Update `execute_script()` in `executor.py`
2. Add file extension mapping
3. Add interpreter command
4. Update documentation

### Custom Execution Environments

- Modify `ScriptExecutor` to use containers
- Add Docker/Podman support
- Implement sandboxing

## Security Considerations

### Script Execution

- **Isolation**: Scripts run in temporary directories
- **Timeouts**: Configurable execution timeouts
- **Sandboxing**: Consider container-based execution for production

### API Keys

- Never log or expose API keys
- Use environment variables or secrets
- Sanitize output

### Generated Scripts

- AI-generated scripts should be reviewed
- Use `--verbose` to see scripts before execution
- Consider approval workflow for production

## Testing Strategy

### Unit Tests

- Test each component independently
- Mock AI responses
- Mock file system operations

### Integration Tests

- Test full workflow
- Use sample documentation
- Verify script generation and execution

### End-to-End Tests

- Test with real AI APIs (separate quota)
- Test with various documentation formats
- Test error scenarios

## Performance Considerations

### AI API Calls

- Batching: Send all documentation in one request
- Caching: Consider caching AI responses
- Rate limiting: Respect API rate limits

### Script Execution

- Parallel execution: Not yet implemented
- Resource limits: Consider adding memory/CPU limits
- Cleanup: Always cleanup temporary resources

## Future Enhancements

### Planned Features

1. **Retry Logic**: Automatic retry for failed scripts
2. **Docker Support**: Run scripts in containers
3. **Parallel Execution**: Execute multiple scripts concurrently
4. **Caching**: Cache AI responses and results
5. **Approval Workflow**: Review scripts before execution
6. **Metrics**: Track success rates and performance
7. **Webhooks**: Notify on completion
8. **Multi-language**: Better support for non-English docs

### Architecture Improvements

1. **Plugin System**: Easy addition of new providers/executors
2. **Event System**: Hook into workflow events
3. **Database**: Store results for analysis
4. **Web UI**: Visual interface for results
5. **API Server**: REST API for integration

## Dependencies

### Core Dependencies

- `requests`: HTTP client for AI APIs and URL fetching
- Python 3.8+: Core language

### Optional Dependencies

- `docker`: For container-based execution
- `pytest`: For testing
- `black`: For code formatting

## Deployment

### Local Installation

```bash
pip install -e .
```

### GitHub Actions

See `.github/workflows/test-docs.yml`

### Docker (Future)

```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -e .
ENTRYPOINT ["doctai"]
```

## Contributing

See component-specific sections above for extension points. Each component is designed to be modular and extensible.

## License

MIT License - See LICENSE file

