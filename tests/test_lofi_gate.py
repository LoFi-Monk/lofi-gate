import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lofi_gate
import pytest
from unittest.mock import MagicMock, patch

def test_determine_test_command_pytest():
    scripts = {}
    with patch("os.path.exists", return_value=True): # Simulates pyproject.toml existing
        cmd = lofi_gate.determine_test_command(scripts)
        assert "pytest" in cmd or "jest" in cmd # fallback or detection

def test_arg_parsing():
    with patch.object(sys, 'argv', ['lofi_gate.py', '--parallel']):
        args = lofi_gate.parse_args()
        assert args.parallel == True
        assert args.serial == False

def test_arg_parsing_default():
    with patch.object(sys, 'argv', ['lofi_gate.py']):
        args = lofi_gate.parse_args()
        assert args.parallel == False
        assert args.serial == True
