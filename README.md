# DSPy Context Synthesizer

Generate tailored `claude.md` files for coding tasks using DSPy and Anthropic's Claude.

## Overview

The DSPy Context Synthesizer automatically generates rich, structured context files that help Claude understand your coding tasks better. It analyzes your task description, existing code examples, and project guidelines to create optimal context for interactive coding sessions.

## Features

- 🎯 **Task-Aware Context Generation**: Tailored context based on specific coding tasks
- 🔧 **Code Pattern Recognition**: Learns from existing code examples
- 📋 **Project Guidelines Integration**: Incorporates project-specific conventions
- 🖥️ **CLI Interface**: Easy-to-use command-line tool
- 🔄 **Interactive Mode**: Step-by-step context generation

## Installation

1. **Prerequisites**: Python 3.8+ and an Anthropic API key

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package**:
   ```bash
   pip install -e .
   ```

4. **Set up your API key**:
   ```bash
   export ANTHROPIC_API_KEY="your-claude-api-key"
   ```

## Quick Start

### Basic Usage

```bash
# Generate context for a coding task
dspy-synthesizer generate \
    --task "Add JWT authentication to FastAPI app" \
    --examples ./examples/code_examples.py \
    --guidelines ./examples/project_guidelines.md
```

### Interactive Mode

```bash
# Launch interactive mode
dspy-synthesizer interactive
```

### Use with Claude CLI

```bash
# After generating context
claude --file claude.md "Implement the authentication system"
```

## Examples

The `examples/` directory contains sample files to get you started:

- `task_example.txt` - Example task description
- `code_examples.py` - Sample code to learn from
- `project_guidelines.md` - Project-specific guidelines

### Example Workflow

1. **Generate context**:
   ```bash
   dspy-synthesizer generate \
       --task "$(cat examples/task_example.txt)" \
       --examples examples/code_examples.py \
       --guidelines examples/project_guidelines.md \
       --output my-context.md
   ```

2. **Review the generated context** in `my-context.md`

3. **Use with Claude**:
   ```bash
   claude --file my-context.md "Help me implement this feature"
   ```

## CLI Reference

### Commands

- `generate` - Generate a context file
- `interactive` - Interactive context generation

### Options

- `--model` - Claude model to use (default: claude-3-sonnet-20240229)
- `--task` - Coding task description
- `--examples` - Path to code examples file
- `--guidelines` - Path to project guidelines file
- `--output` - Output file path (default: claude.md)
- `--preview` - Show preview of generated context

## Configuration

Configuration is stored in `~/.dspy-synthesizer/config.json`. The tool will create default settings on first run.

## Development

### Project Structure

```
dspy-synthesizer/
├── src/dspy_synthesizer/
│   ├── __init__.py
│   ├── synthesizer.py    # Core DSPy module
│   ├── cli.py           # CLI interface
│   └── config.py        # Configuration management
├── examples/            # Example files
├── tests/              # Test files
├── requirements.txt    # Dependencies
└── setup.py           # Package setup
```

### Running Tests

```bash
python -m pytest tests/
```

## Troubleshooting

1. **API Key Issues**: Ensure `ANTHROPIC_API_KEY` is set correctly
2. **Model Access**: Verify your API key has access to the specified Claude model
3. **File Permissions**: Check that output directories are writable

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.