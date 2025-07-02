"""
Ollama model support for DSPy Context Synthesizer
Provides local model alternatives to Anthropic Claude
"""

import dspy
import requests
import json
from typing import Dict, List, Optional


class OllamaModel(dspy.LM):
    """Custom DSPy Language Model for Ollama"""
    
    def __init__(self, model: str = "deepseek-coder:6.7b", base_url: str = "http://localhost:11434", max_tokens: int = 4000, **kwargs):
        super().__init__(model)
        self.model = model
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.kwargs = kwargs
        self.history = []
        
    def basic_request(self, prompt: str, **kwargs) -> str:
        """Basic request method for DSPy compatibility"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": self.max_tokens,
                        "temperature": kwargs.get("temperature", 0.7),
                    }
                },
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            print(f"❌ Ollama generation failed: {e}")
            return ""
    
    def generate(self, prompt: str, **kwargs) -> List[str]:
        """Generate text using Ollama API"""
        result = self.basic_request(prompt, **kwargs)
        return [result] if result else [""]
    
    def __call__(self, prompt: str, **kwargs) -> List[str]:
        """Make the model callable"""
        return self.generate(prompt, **kwargs)


class OllamaContextManager:
    """Manages Ollama model configuration for DSPy"""
    
    # Recommended models for context synthesis
    RECOMMENDED_MODELS = {
        "deepseek-coder:6.7b": {
            "description": "Best for code understanding and context generation",
            "strengths": ["Code analysis", "Technical documentation", "Architecture understanding"],
            "size": "3.8GB"
        },
        "qwen3:8b": {
            "description": "Strong general reasoning and context synthesis",
            "strengths": ["Multi-language support", "Context understanding", "Documentation"],
            "size": "5.2GB"
        },
        "llama3:8b-instruct-q4_0": {
            "description": "Excellent instruction following for structured output",
            "strengths": ["Instruction following", "Structured output", "Context generation"],
            "size": "4.7GB"
        },
        "mistral-openorca:7b-q4_K_M": {
            "description": "Good balance of performance and resource usage",
            "strengths": ["Reasoning", "Context understanding", "Markdown generation"],
            "size": "4.4GB"
        },
        "opencoder:8b": {
            "description": "Specialized for coding tasks and context",
            "strengths": ["Code understanding", "API documentation", "Context synthesis"],
            "size": "4.7GB"
        }
    }
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.configured = False
        
    def check_ollama_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_available_models(self) -> List[str]:
        """Get list of locally available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except:
            pass
        return []
    
    def get_best_available_model(self) -> Optional[str]:
        """Get the best available model for context synthesis"""
        available = self.list_available_models()
        
        # Check recommended models in order of preference
        for model in self.RECOMMENDED_MODELS.keys():
            if model in available:
                return model
        
        # Fallback to any available model that looks suitable
        coding_models = [m for m in available if any(keyword in m.lower() 
                        for keyword in ["coder", "code", "deepseek", "llama3", "qwen", "mistral"])]
        
        if coding_models:
            return coding_models[0]
        
        # Last resort - any available model
        if available:
            return available[0]
            
        return None
    
    def setup_model(self, model_name: Optional[str] = None, max_tokens: int = 4000) -> bool:
        """Configure DSPy with Ollama model"""
        if not self.check_ollama_available():
            print("❌ Ollama is not running. Start it with: ollama serve")
            return False
        
        if not model_name:
            model_name = self.get_best_available_model()
            
        if not model_name:
            print("❌ No suitable Ollama models found")
            print("💡 Install a recommended model:")
            for model, info in self.RECOMMENDED_MODELS.items():
                print(f"   ollama pull {model}  # {info['description']}")
            return False
        
        try:
            ollama_model = OllamaModel(model=model_name, max_tokens=max_tokens)
            dspy.settings.configure(lm=ollama_model)
            self.configured = True
            
            model_info = self.RECOMMENDED_MODELS.get(model_name, {})
            print(f"✅ DSPy configured with Ollama model: {model_name}")
            if model_info:
                print(f"   Description: {model_info.get('description', 'N/A')}")
                print(f"   Strengths: {', '.join(model_info.get('strengths', []))}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ollama model setup failed: {e}")
            return False
    
    def is_configured(self) -> bool:
        """Check if DSPy is configured with Ollama"""
        return self.configured
    
    def print_model_recommendations(self):
        """Print recommendations for Ollama models"""
        print("🤖 Recommended Ollama models for context synthesis:")
        print()
        
        available = self.list_available_models()
        
        for model, info in self.RECOMMENDED_MODELS.items():
            status = "✅ Installed" if model in available else "⬇️  Available"
            print(f"{status} {model} ({info['size']})")
            print(f"   {info['description']}")
            print(f"   Best for: {', '.join(info['strengths'])}")
            if model not in available:
                print(f"   Install: ollama pull {model}")
            print()


def setup_ollama_fallback(prefer_model: str = None) -> bool:
    """
    Setup Ollama as fallback when Anthropic API is not available
    
    Args:
        prefer_model: Preferred model name, auto-selects if None
        
    Returns:
        True if successful, False otherwise
    """
    manager = OllamaContextManager()
    
    if not manager.check_ollama_available():
        print("❌ Ollama not available")
        print("💡 Start Ollama: ollama serve")
        print("💡 Then install a model: ollama pull deepseek-coder:6.7b")
        return False
    
    return manager.setup_model(prefer_model)


def generate_context_simple(task: str, examples: str = "", guidelines: str = "", model: str = "deepseek-coder:6.7b") -> str:
    """
    Simple context generation without DSPy complexity
    Kept as fallback for when DSPy integration fails
    """
    prompt = f"""You are a coding assistant that generates comprehensive context files for Claude AI.

Task Description: {task}

Code Examples: {examples}

Project Guidelines: {guidelines}

Generate a detailed markdown context file that will help Claude understand this coding task. Include:

1. # Project Context
   - Brief overview of the task
   - Technical requirements

2. # Code Examples Analysis
   - Analysis of existing patterns
   - Naming conventions
   - Architecture notes

3. # Implementation Guidelines
   - Step-by-step approach
   - Best practices
   - Error handling

4. # Expected Output
   - What the final code should accomplish
   - Success criteria

Format this as clean, structured markdown that Claude can use as context for the coding task."""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 2000,
                    "temperature": 0.3,
                }
            },
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            return f"Error: HTTP {response.status_code}"
            
    except Exception as e:
        return f"Error: {e}"


def get_ollama_model_info() -> Dict:
    """Get information about available Ollama models"""
    manager = OllamaContextManager()
    available = manager.list_available_models()
    
    return {
        "ollama_running": manager.check_ollama_available(),
        "available_models": available,
        "recommended_models": manager.RECOMMENDED_MODELS,
        "best_available": manager.get_best_available_model()
    }