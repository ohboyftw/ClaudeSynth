"""
Configuration management for DSPy Synthesizer
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for DSPy Synthesizer"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".dspy-synthesizer"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading config: {e}")
        
        # Return default configuration
        return {
            "default_model": "claude-3-sonnet-20240229",
            "max_tokens": 4000,
            "default_output": "claude.md",
            "templates": {
                "fastapi": "FastAPI project with Pydantic models",
                "django": "Django project with REST framework",
                "flask": "Flask web application",
                "general": "General Python project"
            }
        }
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self._config[key] = value
    
    def get_template(self, template_name: str) -> str:
        """Get template guidelines"""
        templates = self.get("templates", {})
        return templates.get(template_name, templates.get("general", ""))
    
    def add_template(self, name: str, description: str) -> None:
        """Add a new template"""
        if "templates" not in self._config:
            self._config["templates"] = {}
        self._config["templates"][name] = description
    
    def list_templates(self) -> Dict[str, str]:
        """List all available templates"""
        return self.get("templates", {})
    
    @property
    def default_model(self) -> str:
        """Get default model"""
        return self.get("default_model", "claude-3-sonnet-20240229")
    
    @property
    def max_tokens(self) -> int:
        """Get max tokens"""
        return self.get("max_tokens", 4000)
    
    @property
    def default_output(self) -> str:
        """Get default output filename"""
        return self.get("default_output", "claude.md")