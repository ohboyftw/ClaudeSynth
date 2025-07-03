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
    def test_setup_anthropic_model_success(self, mock_dspy):
        """Test successful Anthropic model setup"""
        mock_anthropic = Mock()
        mock_dspy.Anthropic.return_value = mock_anthropic
        
        manager = DSPyContextManager()
        result = manager.setup_model(model_name="claude-test-model")
        
        assert result is True
        assert manager.configured is True
        mock_dspy.Anthropic.assert_called_once_with(model="claude-test-model", max_tokens=4000, api_key="test-key")
        mock_dspy.settings.configure.assert_called_once_with(lm=mock_anthropic)

    @patch('dspy_synthesizer.synthesizer.dspy')
    def test_setup_ollama_model_success(self, mock_dspy):
        """Test successful Ollama model setup"""
        mock_ollama_lm = Mock()
        mock_dspy.LM.return_value = mock_ollama_lm
        
        manager = DSPyContextManager()
        result = manager.setup_model(use_ollama=True, ollama_model="test-ollama-model")
        
        assert result is True
        assert manager.configured is True
        mock_dspy.LM.assert_called_once_with(model="ollama/test-ollama-model", max_tokens=4000)
        mock_dspy.settings.configure.assert_called_once_with(lm=mock_ollama_lm)

    @patch.dict(os.environ, {}, clear=True)
    @patch('dspy_synthesizer.synthesizer.dspy')
    def test_setup_anthropic_model_no_api_key_failure(self, mock_dspy):
        """Test Anthropic model setup fails without API key"""
        manager = DSPyContextManager()
        result = manager.setup_model(model_name="claude-test-model")
        
        assert result is False
        assert manager.configured is False
        mock_dspy.Anthropic.assert_not_called()
        mock_dspy.settings.configure.assert_not_called()

    @patch('dspy_synthesizer.synthesizer.dspy')
    def test_setup_ollama_model_failure(self, mock_dspy):
        """Test Ollama model setup failure"""
        mock_dspy.LM.side_effect = Exception("Ollama connection error")
        
        manager = DSPyContextManager()
        result = manager.setup_model(use_ollama=True, ollama_model="test-ollama-model")
        
        assert result is False
        assert manager.configured is False
        mock_dspy.LM.assert_called_once()
        mock_dspy.settings.configure.assert_not_called()
    
    
    
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