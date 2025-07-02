#!/usr/bin/env python3
"""
DSPy Context Synthesizer CLI Tool
Generates tailored claude.md files for coding tasks
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .synthesizer import ContextSynthesizer, DSPyContextManager
from .config import Config


def read_file_content(file_path: str) -> str:
    """Read content from a file safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return ""
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return ""


def _generate_context_simple_mode(args) -> bool:
    """Generate context using simple Ollama mode (no DSPy)"""
    print("📝 Using simple Ollama mode...")
    
    try:
        from .ollama_support import generate_context_simple
        
        # Read input files
        code_examples = ""
        if args.examples:
            code_examples = read_file_content(args.examples)
        
        guidelines = ""
        if args.guidelines:
            guidelines = read_file_content(args.guidelines)
        
        # Generate context using simple mode
        model = args.ollama_model or "deepseek-coder:6.7b"
        context = generate_context_simple(
            task=args.task,
            examples=code_examples,
            guidelines=guidelines,
            model=model
        )
        
        if context.startswith("Error:"):
            print(f"❌ Simple mode generation failed: {context}")
            return False
        
        # Write output
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(context)
        
        print(f"✅ Context generated (simple mode): {output_path}")
        
        # Show preview if requested
        if args.preview:
            print("\n--- Generated Context Preview ---")
            print(context[:500] + "..." if len(context) > 500 else context)
        
        return True
        
    except Exception as e:
        print(f"❌ Simple mode failed: {e}")
        return False


def generate_context(args) -> bool:
    """Generate context file command"""
    print("🔄 Generating context...")
    
    # Handle simple mode for Ollama
    if args.ollama and args.simple_mode:
        return _generate_context_simple_mode(args)
    
    # Setup DSPy (normal or DSPy-integrated Ollama)
    manager = DSPyContextManager()
    use_dspy = not args.simple_mode if args.ollama else True
    
    if args.ollama:
        success = manager._setup_ollama_model(args.ollama_model, use_dspy=use_dspy)
    else:
        success = manager.setup_model(args.model)
    
    if not success:
        return False
    
    # Read input files
    code_examples = ""
    if args.examples:
        code_examples = read_file_content(args.examples)
        if not code_examples:
            print("⚠️ No code examples loaded")
    
    guidelines = ""
    if args.guidelines:
        guidelines = read_file_content(args.guidelines)
        if not guidelines:
            print("⚠️ No guidelines loaded")
    
    # Generate context
    synthesizer = ContextSynthesizer()
    try:
        result = synthesizer.forward(
            task_description=args.task,
            code_examples=code_examples,
            project_guidelines=guidelines
        )
        
        # Write output
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.markdown_context)
        
        print(f"✅ Context generated: {output_path}")
        
        # Show preview if requested
        if args.preview:
            print("\n--- Generated Context Preview ---")
            print(result.markdown_context[:500] + "..." if len(result.markdown_context) > 500 else result.markdown_context)
        
        return True
        
    except Exception as e:
        print(f"❌ Context generation failed: {e}")
        return False


def interactive_mode(args) -> bool:
    """Interactive mode for generating contexts"""
    print("🎯 Interactive Context Generation Mode")
    print("Enter 'quit' to exit\n")
    
    # Setup DSPy
    manager = DSPyContextManager()
    if not manager.setup_model(args.model, use_ollama=args.ollama, ollama_model=args.ollama_model):
        return False
    
    synthesizer = ContextSynthesizer()
    
    while True:
        try:
            # Get task description
            task = input("📝 Enter coding task description: ").strip()
            if task.lower() == 'quit':
                break
            
            if not task:
                print("⚠️ Task description cannot be empty")
                continue
            
            # Optional code examples
            examples_path = input("📁 Code examples file (optional, press Enter to skip): ").strip()
            examples = ""
            if examples_path:
                examples = read_file_content(examples_path)
            
            # Optional guidelines
            guidelines_path = input("📋 Guidelines file (optional, press Enter to skip): ").strip()
            guidelines = ""
            if guidelines_path:
                guidelines = read_file_content(guidelines_path)
            
            # Generate context
            print("\n🔄 Generating context...")
            result = synthesizer.forward(
                task_description=task,
                code_examples=examples,
                project_guidelines=guidelines
            )
            
            # Save output
            output_file = f"claude-context-{len(task.split()[:3])}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.markdown_context)
            
            print(f"✅ Context saved to: {output_file}")
            print(f"💡 Next step: Use with Claude CLI: claude --file {output_file}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    return True


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="DSPy Context Synthesizer - Generate tailored claude.md files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate context for a specific task
  dspy-synthesizer generate --task "Add JWT authentication" --examples ./src/auth.py
  
  # Interactive mode
  dspy-synthesizer interactive
  
  # Use with custom model
  dspy-synthesizer generate --model claude-3-opus-20240229 --task "Implement REST API"
        """
    )
    
    parser.add_argument("--model", default="claude-3-sonnet-20240229", 
                       help="Claude model to use (default: claude-3-sonnet-20240229)")
    parser.add_argument("--ollama", action="store_true",
                       help="Use Ollama instead of Anthropic Claude")
    parser.add_argument("--ollama-model", 
                       help="Specific Ollama model to use (auto-selects best if not specified)")
    parser.add_argument("--list-ollama", action="store_true",
                       help="List available Ollama models and recommendations")
    parser.add_argument("--version", action="version", version="dspy-synthesizer 0.1.0")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate context file')
    gen_parser.add_argument('--task', required=True, 
                           help='Coding task description')
    gen_parser.add_argument('--examples', 
                           help='Path to file containing code examples')
    gen_parser.add_argument('--guidelines', 
                           help='Path to file containing project guidelines')
    gen_parser.add_argument('--output', default='claude.md', 
                           help='Output file path (default: claude.md)')
    gen_parser.add_argument('--preview', action='store_true',
                           help='Show preview of generated context')
    gen_parser.add_argument('--ollama', action='store_true',
                           help='Use Ollama instead of Anthropic Claude')
    gen_parser.add_argument('--ollama-model', 
                           help='Specific Ollama model to use')
    gen_parser.add_argument('--simple-mode', action='store_true',
                           help='Use simple Ollama mode (bypass DSPy features)')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Interactive mode')
    interactive_parser.add_argument('--ollama', action='store_true',
                                   help='Use Ollama instead of Anthropic Claude')
    interactive_parser.add_argument('--ollama-model', 
                                   help='Specific Ollama model to use')
    interactive_parser.add_argument('--simple-mode', action='store_true',
                                   help='Use simple Ollama mode (bypass DSPy features)')
    
    args = parser.parse_args()
    
    # Handle special commands first
    if args.list_ollama:
        from .ollama_support import OllamaContextManager
        manager = OllamaContextManager()
        manager.print_model_recommendations()
        print("\n🎯 Proper DSPy Integration Available:")
        print("All models work with: dspy.LM(model='ollama/model-name')")
        return
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    success = False
    if args.command == 'generate':
        success = generate_context(args)
    elif args.command == 'interactive':
        success = interactive_mode(args)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()