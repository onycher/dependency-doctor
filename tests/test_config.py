import os
import pytest
from src.utils.config import get_config

def test_get_config_existing(monkeypatch):
    monkeypatch.setenv("TEST_KEY", "test_value")
    assert get_config("TEST_KEY") == "test_value"

def test_get_config_missing(monkeypatch):
    monkeypatch.delenv("MISSING_KEY", raising=False)
    assert get_config("MISSING_KEY") is None

def test_get_config_default(monkeypatch):
    monkeypatch.delenv("DEFAULT_KEY", raising=False)
    assert get_config("DEFAULT_KEY", default="default_value") == "default_value" 