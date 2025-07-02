#!/usr/bin/env python3
"""
Simple test of Ollama integration without full DSPy complexity
"""

import sys
import os
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_ollama_direct():
    """Test direct Ollama API call"""
    print("🧪 Testing direct Ollama API...")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-coder:6.7b",
                "prompt": """Generate a markdown context file for a coding task. 

Task: Create a simple REST API endpoint for user management

The context should include:
- Project overview
- API design guidelines  
- Code examples
- Best practices

Format as markdown with clear sections.""",
                "stream": False,
                "options": {
                    "num_predict": 1000,
                    "temperature": 0.7,
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            context = result.get("response", "")
            
            # Save to file
            with open("test-direct-ollama.md", "w") as f:
                f.write(context)
            
            print("✅ Direct Ollama test successful!")
            print(f"📄 Context saved to: test-direct-ollama.md")
            print(f"📊 Generated {len(context)} characters")
            print("\n--- Preview ---")
            print(context[:500] + "..." if len(context) > 500 else context)
            return True
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Direct Ollama test failed: {e}")
        return False

def test_simple_context_generator():
    """Test a simple context generator without DSPy complexity"""
    print("\n🧪 Testing simple context generator...")
    
    def generate_context_simple(task, examples="", guidelines=""):
        """Simple context generation"""
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
                    "model": "deepseek-coder:6.7b",
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
    
    # Test with example task
    task = "Create a FastAPI endpoint for user authentication with JWT tokens"
    examples = """
# Existing code example
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str
    
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "username": "example"}
"""
    
    guidelines = """
- Use Pydantic models for request/response
- Include proper error handling
- Add type hints for all functions
- Follow REST API conventions
"""
    
    context = generate_context_simple(task, examples, guidelines)
    
    if context.startswith("Error:"):
        print(f"❌ Simple generator failed: {context}")
        return False
    else:
        # Save result
        with open("test-simple-generator.md", "w") as f:
            f.write(context)
        
        print("✅ Simple generator successful!")
        print(f"📄 Context saved to: test-simple-generator.md")
        print(f"📊 Generated {len(context)} characters")
        print("\n--- Preview ---")
        print(context[:500] + "..." if len(context) > 500 else context)
        return True

if __name__ == "__main__":
    print("🚀 Testing Ollama Integration for DSPy Synthesizer")
    print("=" * 60)
    
    success1 = test_ollama_direct()
    success2 = test_simple_context_generator()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 All Ollama tests passed!")
        print("\n💡 Next steps:")
        print("1. Use the working simple generator as fallback")
        print("2. Check generated files: test-direct-ollama.md, test-simple-generator.md")
        print("3. Integrate simple approach into DSPy synthesizer")
    else:
        print("❌ Some tests failed")
        if not success1:
            print("   - Direct Ollama API test failed")
        if not success2:  
            print("   - Simple generator test failed")
        print("\n💡 Troubleshooting:")
        print("   - Check if Ollama is running: ollama serve")
        print("   - Check if model is available: ollama list")
        print("   - Try: ollama pull deepseek-coder:6.7b")