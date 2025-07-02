"""
DSPy Context Synthesizer
Generates tailored claude.md files for coding tasks using DSPy
"""

__version__ = "0.1.0"
__author__ = "DSPy Synthesizer Team"

from .synthesizer import ContextSynthesizer, ContextSignature
from .cli import main

__all__ = ["ContextSynthesizer", "ContextSignature", "main"]