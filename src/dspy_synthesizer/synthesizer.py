"""
Core DSPy Context Synthesizer module
"""

import dspy
import os
from typing import Optional, Dict, Any


class ContextSignature(dspy.Signature):
    """
    Analyzes a coding task and existing code examples to generate a
    well-structured markdown context file (`claude.md`).
    This context should guide a developer's interactive session with Claude
    by outlining conventions, relevant components, and style.
    """
    task_description = dspy.InputField(
        desc="A high-level description of the new coding feature to implement."
    )
    code_examples = dspy.InputField(
        desc="One or more snippets of existing code from the project to infer conventions from."
    )
    project_guidelines = dspy.InputField(
        desc="General project-wide guidelines or constraints."
    )
    markdown_context = dspy.OutputField(
        desc="A comprehensive, well-structured markdown file content that will serve as the context for an interactive coding session."
    )


class ContextSynthesizer(dspy.Module):
    """A DSPy module that synthesizes the ideal context for a coding task."""
    
    def __init__(self):
        super().__init__()
        # ChainOfThought is used to encourage the LLM to "reason" about what
        # makes good context before producing the final markdown file.
        self.synthesizer = dspy.ChainOfThought(ContextSignature)

    def forward(self, task_description: str, code_examples: str = "", project_guidelines: str = ""):
        """
        Generate context for a coding task
        
        Args:
            task_description: Description of the coding task
            code_examples: Existing code examples to learn from
            project_guidelines: Project-specific guidelines
            
        Returns:
            DSPy result with markdown_context field
        """
        result = self.synthesizer(
            task_description=task_description,
            code_examples=code_examples,
            project_guidelines=project_guidelines
        )
        return result


class DSPyContextManager:
    """Manages DSPy configuration and model setup"""
    
    def __init__(self):
        self.configured = False
        
    def setup_model(self, model_name: str = "claude-3-sonnet-20240229", max_tokens: int = 4000, use_ollama: bool = False, ollama_model: str = None) -> bool:
        """
        Configure DSPy with Anthropic Claude or Ollama
        
        Args:
            model_name: Claude model to use
            max_tokens: Maximum tokens for generation
            use_ollama: Whether to use Ollama instead of Anthropic
            ollama_model: Specific Ollama model to use
            
        Returns:
            True if successful, False otherwise
        """
        if use_ollama:
            return self._setup_ollama_model(ollama_model, max_tokens)
        else:
            return self._setup_anthropic_model(model_name, max_tokens)
    
    def _setup_anthropic_model(self, model_name: str, max_tokens: int) -> bool:
        """Setup Anthropic Claude model"""
        try:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable required")
            
            claude_model = dspy.Anthropic(model=model_name, max_tokens=max_tokens, api_key=api_key)
            dspy.settings.configure(lm=claude_model)
            self.configured = True
            print(f"✅ DSPy configured with {model_name}")
            return True
            
        except Exception as e:
            print(f"❌ Anthropic setup failed: {e}")
            
    
    def _setup_ollama_model(self, ollama_model: str = None, max_tokens: int = 4000) -> bool:
        """Setup Ollama model using proper DSPy integration"""
        try:
            # Use proper DSPy LM with LiteLLM integration
            model_name = ollama_model or "deepseek-coder:6.7b"
            
            # DSPy's proper way via LiteLLM
            ollama_lm = dspy.LM(model=f"ollama/{model_name}", max_tokens=max_tokens)
            dspy.settings.configure(lm=ollama_lm)
            
            self.configured = True
            print(f"🎯 Using proper DSPy + Ollama integration: {model_name}")
            print("✨ Full DSPy features: ChainOfThought, optimization, caching")
            return True
            
        except Exception as e:
            print(f"❌ Proper DSPy-Ollama setup failed: {e}")
            return False
    
    
    
    def is_configured(self) -> bool:
        """Check if DSPy is properly configured"""
        return self.configured