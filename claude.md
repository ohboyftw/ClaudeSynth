# DSPy Context Synthesizer - MVP Project

## Project Overview

A minimum viable product for generating tailored `claude.md` files using DSPy and Anthropic's Claude. This tool automatically creates rich, structured context files that help Claude understand coding tasks better.

## Key Implementation Notes

- **Always use `python3`** instead of `python` for all commands
- **Virtual Environment**: Use `dspy-env` (not `venv`) for consistency
- **Package Structure**: Standard Python package in `src/dspy_synthesizer/`
- **Dependencies**: `dspy-ai`, `anthropic`, `openai` (installed and working)

## Project Structure

```
dspy-synthesizer/
├── src/dspy_synthesizer/
│   ├── __init__.py           # Package initialization
│   ├── synthesizer.py        # Core DSPy modules
│   ├── cli.py               # Command-line interface
│   └── config.py            # Configuration management
├── examples/                 # Sample usage files
│   ├── task_example.txt     # Example task description
│   ├── code_examples.py     # Sample code to learn from
│   └── project_guidelines.md # Project guidelines
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_synthesizer.py
├── dspy-env/               # Virtual environment (working)
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
├── README.md              # Documentation
├── test_simple.py         # MVP test script
└── claude.md              # This file
```

## Core Components

### 1. ContextSynthesizer (synthesizer.py)
- `ContextSignature`: DSPy signature defining input/output schema
- `ContextSynthesizer`: Main DSPy module using ChainOfThought
- `DSPyContextManager`: Handles model configuration and setup

### 2. CLI Interface (cli.py)
- `generate` command: Create context files
- `interactive` command: Step-by-step context generation
- Supports file inputs for examples and guidelines

### 3. Configuration (config.py)
- User preferences stored in `~/.dspy-synthesizer/config.json`
- Template system for different project types
- Default model and token settings

## Activation and Usage

### Environment Setup
```bash
# Always activate the environment first
source dspy-env/bin/activate

# Option 1: Use Anthropic Claude (requires API key)
export ANTHROPIC_API_KEY="your-api-key"

# Option 2: Use Ollama (local models, no API key needed)
# Make sure Ollama is running: ollama serve
```

### CLI Commands

#### With Anthropic Claude
```bash
# Generate context with Claude
PYTHONPATH=src python3 -m dspy_synthesizer.cli generate \
    --task "Add JWT authentication to FastAPI app" \
    --examples examples/code_examples.py \
    --guidelines examples/project_guidelines.md
```

#### With Ollama (Local Models)
```bash
# List available Ollama models and recommendations
PYTHONPATH=src python3 -m dspy_synthesizer.cli --list-ollama

# Generate context with Ollama (auto-selects best model)
PYTHONPATH=src python3 -m dspy_synthesizer.cli generate \
    --ollama \
    --task "Add JWT authentication to FastAPI app" \
    --examples examples/code_examples.py

# Use specific Ollama model
PYTHONPATH=src python3 -m dspy_synthesizer.cli generate \
    --ollama --ollama-model "deepseek-coder:6.7b" \
    --task "Create REST API endpoints"

# Interactive mode with Ollama
PYTHONPATH=src python3 -m dspy_synthesizer.cli interactive --ollama
```

### Testing
```bash
# Run MVP tests (no API key needed)
python3 test_simple.py
```

## MVP Status: ✅ WORKING

All core functionality implemented and tested:
- ✅ Package structure created
- ✅ Core DSPy modules implemented
- ✅ CLI interface working
- ✅ Configuration system ready
- ✅ Example files provided
- ✅ Tests passing
- ✅ Virtual environment configured
- ✅ Dependencies installed correctly
- ✅ **Ollama integration working** - Local model support added
- ✅ **Multiple model backends** - Anthropic Claude + Ollama options

## Available Ollama Models (✅ All Installed)

**Recommended for Context Synthesis:**
- `deepseek-coder:6.7b` - Best for code understanding (3.8GB)
- `qwen3:8b` - Strong reasoning and documentation (5.2GB)  
- `llama3:8b-instruct-q4_0` - Excellent instruction following (4.7GB)
- `mistral-openorca:7b-q4_K_M` - Balanced performance (4.4GB)
- `opencoder:8b` - Specialized for coding tasks (4.7GB)

## Next Development Steps

1. **API Integration Testing**: Test with real Anthropic API key
2. **Compiled Behaviors**: Add training/optimization pipeline
3. **Project Templates**: Expand template system
4. **Validation**: Add context quality metrics
5. **Integration**: Direct Claude CLI integration

## Usage Examples

### Basic Context Generation
```bash
source dspy-env/bin/activate
export ANTHROPIC_API_KEY="your-key"
PYTHONPATH=src python3 -m dspy_synthesizer.cli generate \
    --task "$(cat examples/task_example.txt)" \
    --examples examples/code_examples.py \
    --output my-context.md
```

### With Claude CLI
```bash
# After generating context
claude --file my-context.md "Help me implement this feature"
```

### Working Ollama Examples
```bash
# Test Ollama integration directly
python3 test_ollama_simple.py

# List available models
PYTHONPATH=src python3 -m dspy_synthesizer.cli --list-ollama

# Generate with best available model
PYTHONPATH=src python3 -m dspy_synthesizer.cli generate \
    --ollama \
    --task "Create a FastAPI user authentication system" \
    --output auth-context.md
```

## Key Features Delivered

🎯 **Dual Backend Support**: 
- Anthropic Claude for production use
- Ollama for local development (no API costs)

🤖 **True DSPy Integration**:
- ✅ **Proper approach**: `dspy.LM(model="ollama/model-name")` via LiteLLM
- ❌ **My mistake**: Custom LM adapter (overcomplicated)
- 🧠 **ChainOfThought reasoning**: Full DSPy benefits with Ollama
- 📊 **Built-in optimization**: Caching, retries, signature validation

📝 **Context Quality**:
- Structured markdown output with reasoning chains
- Task-aware generation using DSPy signatures  
- Code pattern recognition via ChainOfThought

🔧 **Implementation Status**:
- ✅ Simple mode: Working (direct Ollama calls)
- ✅ Proper DSPy: Working (`dspy.LM` with `ollama/model`)
- ❌ Custom adapter: Overcomplicated (should be replaced)

## 🎓 Key Learning

**The correct way to use Ollama with DSPy:**
```python
# Simple and proper
llm = dspy.LM(model="ollama/deepseek-coder:6.7b", max_tokens=4000)
dspy.settings.configure(lm=llm)

# Then use standard DSPy modules
synthesizer = dspy.ChainOfThought(ContextSignature)
```

This provides **full DSPy functionality** with Ollama models, including reasoning chains, automatic optimization, and signature validation.

See `EVALUATION.md` for detailed analysis of implementation approaches.