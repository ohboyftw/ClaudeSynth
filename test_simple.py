#!/usr/bin/env python3
"""
Simple test script for DSPy Context Synthesizer
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test basic imports"""
    try:
        import dspy
        print("✅ DSPy imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import DSPy: {e}")
        return False
    
    try:
        from dspy_synthesizer.synthesizer import ContextSynthesizer, DSPyContextManager
        print("✅ ContextSynthesizer imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ContextSynthesizer: {e}")
        return False
    
    try:
        from dspy_synthesizer.config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Config: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without API calls"""
    try:
        from dspy_synthesizer.synthesizer import ContextSynthesizer, DSPyContextManager
        from dspy_synthesizer.config import Config
        
        # Test config
        config = Config()
        print(f"✅ Config created with default model: {config.default_model}")
        
        # Test context manager creation
        manager = DSPyContextManager()
        print(f"✅ DSPyContextManager created, configured: {manager.is_configured()}")
        
        # Test synthesizer creation
        synthesizer = ContextSynthesizer()
        print("✅ ContextSynthesizer created")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_cli():
    """Test CLI help without API calls"""
    try:
        from dspy_synthesizer.cli import main
        print("✅ CLI module imported successfully")
        
        # Test help (this will exit, so we wrap it)
        old_argv = sys.argv
        try:
            sys.argv = ['dspy-synthesizer', '--help']
            main()
        except SystemExit:
            print("✅ CLI help executed successfully")
        finally:
            sys.argv = old_argv
            
        return True
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing DSPy Context Synthesizer MVP")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing imports...")
    success &= test_imports()
    
    print("\n2. Testing basic functionality...")
    success &= test_basic_functionality()
    
    print("\n3. Testing CLI...")
    success &= test_cli()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! MVP is ready for testing.")
        print("\nNext steps:")
        print("1. Set ANTHROPIC_API_KEY environment variable")
        print("2. Run: python test_with_api.py (when API key is available)")
        print("3. Try: PYTHONPATH=src python -m dspy_synthesizer.cli --help")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    sys.exit(0 if success else 1)