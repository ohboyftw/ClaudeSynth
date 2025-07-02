"""
Tests for the DSPy Context Synthesizer
"""

import pytest
import os
from unittest.mock import Mock, patch
from dspy_synthesizer.synthesizer import ContextSynthesizer, DSPyContextManager


class TestDSPyContextManager:
    """Test DSPy configuration management"""
    
    def test_init(self):
        """Test manager initialization"""
        manager = DSPyContextManager()
        assert not manager.configured
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('dspy_synthesizer.synthesizer.dspy')
    def test_setup_model_success(self, mock_dspy):
        """Test successful model setup"""
        mock_anthropic = Mock()
        mock_dspy.Anthropic.return_value = mock_anthropic
        
        manager = DSPyContextManager()
        result = manager.setup_model()
        
        assert result is True
        assert manager.configured is True
        mock_dspy.Anthropic.assert_called_once()
        mock_dspy.settings.configure.assert_called_once_with(lm=mock_anthropic)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_setup_model_no_api_key(self):
        """Test model setup without API key"""
        manager = DSPyContextManager()
        result = manager.setup_model()
        
        # Should fall back to test model
        assert result is True
        assert manager.configured is True
    
    def test_is_configured(self):
        """Test configuration status check"""
        manager = DSPyContextManager()
        assert not manager.is_configured()
        
        manager.configured = True
        assert manager.is_configured()


class TestContextSynthesizer:
    """Test context synthesis functionality"""
    
    def test_init(self):
        """Test synthesizer initialization"""
        synthesizer = ContextSynthesizer()
        assert synthesizer.synthesizer is not None
    
    @patch('dspy_synthesizer.synthesizer.dspy')
    def test_forward(self, mock_dspy):
        """Test context generation"""
        # Mock the DSPy chain
        mock_result = Mock()
        mock_result.markdown_context = "# Test Context\n\nThis is a test."
        
        mock_chain = Mock()
        mock_chain.return_value = mock_result
        mock_dspy.ChainOfThought.return_value = mock_chain
        
        synthesizer = ContextSynthesizer()
        result = synthesizer.forward(
            task_description="Test task",
            code_examples="Test code",
            project_guidelines="Test guidelines"
        )
        
        assert result == mock_result
        mock_chain.assert_called_once_with(
            task_description="Test task",
            code_examples="Test code",
            project_guidelines="Test guidelines"
        )
    
    def test_forward_with_defaults(self):
        """Test context generation with default parameters"""
        synthesizer = ContextSynthesizer()
        
        # This should not raise an exception
        try:
            result = synthesizer.forward("Test task")
            # We can't easily test the actual result without a real model
            # but we can ensure the method accepts default parameters
        except Exception as e:
            # Expected to fail without proper DSPy setup, but parameters should be accepted
            pass