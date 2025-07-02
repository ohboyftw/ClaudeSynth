#!/usr/bin/env python3
"""
Test script comparing DSPy-integrated Ollama vs Simple Ollama mode
Demonstrates the differences in functionality and output quality
"""

import sys
import os
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_dspy_integration():
    """Test true DSPy integration with Ollama"""
    print("🎯 Testing DSPy-Integrated Ollama Mode")
    print("-" * 50)
    
    try:
        # Import DSPy components
        import dspy
        from dspy_synthesizer.ollama_dspy_adapter import setup_dspy_ollama, get_ollama_dspy_info
        from dspy_synthesizer.synthesizer import ContextSynthesizer, ContextSignature
        
        # Check available models
        info = get_ollama_dspy_info()
        print(f"Ollama running: {info['ollama_running']}")
        print(f"Best model for DSPy: {info['best_for_dspy']}")
        print(f"DSPy-ready models: {info['installed_dspy_ready']}")
        
        if not info['ollama_running']:
            print("❌ Ollama not running")
            return False
        
        # Setup DSPy with Ollama
        print("\n🔧 Setting up DSPy with Ollama...")
        success = setup_dspy_ollama(mode="dspy", temperature=0.3)
        
        if not success:
            print("❌ DSPy-Ollama setup failed")
            return False
        
        print("✅ DSPy-Ollama setup successful")
        
        # Test DSPy Chain of Thought
        print("\n🧠 Testing DSPy ChainOfThought...")
        synthesizer = ContextSynthesizer()
        
        task = "Create a REST API endpoint for user authentication with JWT tokens"
        examples = """
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str
"""
        guidelines = "Use Pydantic models, include error handling, follow REST conventions"
        
        start_time = time.time()
        try:
            result = synthesizer.forward(
                task_description=task,
                code_examples=examples,
                project_guidelines=guidelines
            )
            
            elapsed = time.time() - start_time
            context = result.markdown_context
            
            # Save result
            with open("test-dspy-mode.md", "w") as f:
                f.write(context)
            
            print(f"✅ DSPy generation completed in {elapsed:.1f}s")
            print(f"📄 Generated {len(context)} characters")
            print(f"💾 Saved to: test-dspy-mode.md")
            
            # Show characteristics of DSPy output
            print("\n🔍 DSPy Output Analysis:")
            print(f"  - Contains reasoning chains: {'chain of thought' in context.lower() or 'reasoning' in context.lower()}")
            print(f"  - Structured format: {'#' in context and '##' in context}")
            print(f"  - Code analysis: {'code' in context.lower() and 'analysis' in context.lower()}")
            
            print("\n--- DSPy Output Preview ---")
            print(context[:400] + "..." if len(context) > 400 else context)
            
            return True
            
        except Exception as e:
            print(f"❌ DSPy generation failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ DSPy import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ DSPy test failed: {e}")
        return False


def test_simple_mode():
    """Test simple Ollama mode without DSPy"""
    print("\n\n📝 Testing Simple Ollama Mode")
    print("-" * 50)
    
    try:
        from dspy_synthesizer.ollama_support import generate_context_simple
        
        task = "Create a REST API endpoint for user authentication with JWT tokens"
        examples = """
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str
"""
        guidelines = "Use Pydantic models, include error handling, follow REST conventions"
        
        print("🔧 Generating context with simple mode...")
        start_time = time.time()
        
        context = generate_context_simple(
            task=task,
            examples=examples,
            guidelines=guidelines,
            model="deepseek-coder:6.7b"
        )
        
        elapsed = time.time() - start_time
        
        if context.startswith("Error:"):
            print(f"❌ Simple mode failed: {context}")
            return False
        
        # Save result
        with open("test-simple-mode.md", "w") as f:
            f.write(context)
        
        print(f"✅ Simple generation completed in {elapsed:.1f}s")
        print(f"📄 Generated {len(context)} characters")
        print(f"💾 Saved to: test-simple-mode.md")
        
        # Show characteristics of simple output
        print("\n🔍 Simple Mode Analysis:")
        print(f"  - Direct response: {not ('chain of thought' in context.lower())}")
        print(f"  - Structured format: {'#' in context and '##' in context}")
        print(f"  - Focused content: {'implementation' in context.lower()}")
        
        print("\n--- Simple Mode Preview ---")
        print(context[:400] + "..." if len(context) > 400 else context)
        
        return True
        
    except Exception as e:
        print(f"❌ Simple mode test failed: {e}")
        return False


def compare_outputs():
    """Compare the outputs from both modes"""
    print("\n\n📊 Comparing DSPy vs Simple Mode Outputs")
    print("=" * 60)
    
    dspy_file = Path("test-dspy-mode.md")
    simple_file = Path("test-simple-mode.md")
    
    if not dspy_file.exists() or not simple_file.exists():
        print("❌ Output files not found for comparison")
        return
    
    dspy_content = dspy_file.read_text()
    simple_content = simple_file.read_text()
    
    print(f"DSPy Mode Output:")
    print(f"  📏 Length: {len(dspy_content)} characters")
    print(f"  📝 Lines: {len(dspy_content.splitlines())}")
    print(f"  🏗️  Structure: {dspy_content.count('#')} headers")
    
    print(f"\nSimple Mode Output:")
    print(f"  📏 Length: {len(simple_content)} characters")
    print(f"  📝 Lines: {len(simple_content.splitlines())}")
    print(f"  🏗️  Structure: {simple_content.count('#')} headers")
    
    # Key differences
    print(f"\n🔄 Key Differences:")
    dspy_keywords = ["reasoning", "chain", "analysis", "step-by-step"]
    simple_keywords = ["implementation", "direct", "straightforward"]
    
    dspy_reasoning = sum(1 for kw in dspy_keywords if kw in dspy_content.lower())
    simple_directness = sum(1 for kw in simple_keywords if kw in simple_content.lower())
    
    print(f"  DSPy reasoning indicators: {dspy_reasoning}")
    print(f"  Simple directness indicators: {simple_directness}")
    
    print(f"\n💡 Recommendations:")
    print(f"  🎯 Use DSPy mode for: Complex reasoning, structured analysis, optimization")
    print(f"  📝 Use Simple mode for: Quick generation, resource constraints, simple tasks")


def test_cli_commands():
    """Test CLI commands for both modes"""
    print("\n\n🖥️  CLI Command Examples")
    print("=" * 60)
    
    print("DSPy Mode Commands:")
    print("# Full DSPy integration with ChainOfThought")
    print("PYTHONPATH=src python3 -m dspy_synthesizer.cli generate \\")
    print("    --ollama --task 'Create FastAPI auth endpoint' \\")
    print("    --output dspy-result.md")
    
    print("\nSimple Mode Commands:")
    print("# Bypass DSPy, direct Ollama calls")
    print("PYTHONPATH=src python3 -m dspy_synthesizer.cli generate \\")
    print("    --ollama --simple-mode --task 'Create FastAPI auth endpoint' \\")
    print("    --output simple-result.md")
    
    print("\nModel Selection:")
    print("# List DSPy-compatible models")
    print("PYTHONPATH=src python3 -m dspy_synthesizer.cli --list-ollama")
    
    print("\n# Use specific model")
    print("PYTHONPATH=src python3 -m dspy_synthesizer.cli generate \\")
    print("    --ollama --ollama-model 'qwen3:8b' --task 'Your task'")


if __name__ == "__main__":
    print("🚀 DSPy vs Simple Mode Comparison Test")
    print("=" * 60)
    
    # Test both modes
    dspy_success = test_dspy_integration()
    simple_success = test_simple_mode()
    
    # Compare if both succeeded
    if dspy_success and simple_success:
        compare_outputs()
    
    # Show CLI examples
    test_cli_commands()
    
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print(f"  DSPy Mode: {'✅ Working' if dspy_success else '❌ Failed'}")
    print(f"  Simple Mode: {'✅ Working' if simple_success else '❌ Failed'}")
    
    if dspy_success and simple_success:
        print("\n🎉 Both modes working! You have full flexibility:")
        print("  🎯 DSPy mode: Full reasoning, structured analysis, optimization potential")
        print("  📝 Simple mode: Fast generation, lower resource usage, direct output")
    elif simple_success:
        print("\n⚠️  Simple mode working, DSPy mode failed:")
        print("  📝 You can still generate contexts, but without DSPy's advanced features")
    else:
        print("\n❌ Both modes failed - check Ollama setup")
        print("  💡 Make sure Ollama is running: ollama serve")
        print("  💡 Install a model: ollama pull deepseek-coder:6.7b")