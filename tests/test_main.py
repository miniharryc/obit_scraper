"""
Tests for the main module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from main import hello_world


class TestHelloWorld:
    """Test cases for hello_world function."""
    
    def test_hello_world_default(self):
        """Test hello_world with default parameter."""
        result = hello_world()
        assert result == "Hello, World!"
    
    def test_hello_world_with_name(self):
        """Test hello_world with custom name."""
        result = hello_world("Python")
        assert result == "Hello, Python!"
    
    def test_hello_world_empty_string(self):
        """Test hello_world with empty string."""
        result = hello_world("")
        assert result == "Hello, !"
    
    def test_hello_world_special_characters(self):
        """Test hello_world with special characters."""
        result = hello_world("Test-User_123")
        assert result == "Hello, Test-User_123!"
