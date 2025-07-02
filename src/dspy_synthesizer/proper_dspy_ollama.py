"""
Proper DSPy integration using built-in dspy.OllamaLocal
Based on standard DSPy patterns and best practices
"""

import dspy
from typing import Optional


def setup_proper_dspy_ollama(model: str = "deepseek-coder:6.7b", max_tokens: int = 4000) -> bool:
    """
    Setup DSPy using proper LiteLLM integration
    This is the CORRECT way to use Ollama with modern DSPy
    """
    try:
        # Use DSPy's LM class with ollama provider (via LiteLLM)
        llm = dspy.LM(model=f"ollama/{model}", max_tokens=max_tokens)
        dspy.settings.configure(lm=llm)
        
        print(f"✅ DSPy configured properly with Ollama via LiteLLM: {model}")
        return True
        
    except Exception as e:
        print(f"❌ Proper DSPy LM setup failed: {e}")
        return False


class ProperContextSynthesizer(dspy.Module):
    """
    Proper DSPy module following standard patterns
    Uses built-in DSPy components instead of custom implementations
    """
    
    def __init__(self):
        super().__init__()
        # Use DSPy's ChainOfThought with our signature
        self.synthesizer = dspy.ChainOfThought(ContextSignature)
    
    def forward(self, task_description: str, code_examples: str = "", project_guidelines: str = ""):
        """
        Forward pass using standard DSPy patterns
        """
        # Let DSPy handle the prompting and reasoning
        result = self.synthesizer(
            task_description=task_description,
            code_examples=code_examples,
            project_guidelines=project_guidelines
        )
        return result


class ContextSignature(dspy.Signature):
    """
    DSPy signature defining the context synthesis task
    This is the proper way to define input/output schema in DSPy
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


def test_proper_dspy_integration():
    """
    Test proper DSPy integration following standard patterns
    """
    print("🎯 Testing Proper DSPy Integration")
    print("-" * 50)
    
    # Setup using built-in DSPy components
    success = setup_proper_dspy_ollama("deepseek-coder:6.7b")
    
    if not success:
        print("❌ Could not setup built-in DSPy OllamaLocal")
        return False
    
    # Use proper DSPy module
    synthesizer = ProperContextSynthesizer()
    
    try:
        # Test the pipeline
        result = synthesizer.forward(
            task_description="Create a FastAPI endpoint for user authentication",
            code_examples="""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str
""",
            project_guidelines="Use Pydantic models, include error handling"
        )
        
        print("✅ Proper DSPy integration successful!")
        print(f"📄 Generated context: {len(result.markdown_context)} characters")
        
        # Save result
        with open("proper-dspy-result.md", "w") as f:
            f.write(result.markdown_context)
        
        print("💾 Saved to: proper-dspy-result.md")
        
        # Show DSPy's internal history/reasoning
        if hasattr(dspy.settings.lm, 'inspect_history'):
            print("\n🔍 DSPy Interaction History:")
            dspy.settings.lm.inspect_history(n=1)
        
        return True
        
    except Exception as e:
        print(f"❌ Proper DSPy test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_proper_dspy_integration()
    
    if success:
        print("\n🎉 Proper DSPy integration working!")
        print("💡 This is the correct way to use DSPy with Ollama")
    else:
        print("\n⚠️ Built-in DSPy OllamaLocal not available")
        print("💡 May need to use custom adapter as fallback")