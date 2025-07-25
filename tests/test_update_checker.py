import pytest
from unittest.mock import patch
from src.services.update_checker import check_for_updates

# Mock data for PyPI responses
PYPI_MOCK_DATA = {
    "click": "8.2.1",
    "requests": "2.28.1",
    "werkzeug": "3.1.3",
}

@pytest.fixture
def mock_pypi_api(monkeypatch):
    def mock_get_latest_version(package_name):
        return PYPI_MOCK_DATA.get(package_name)

    monkeypatch.setattr(
        "src.services.update_checker.get_latest_version",
        mock_get_latest_version
    )

def test_outdated_dependencies(mock_pypi_api):
    deps = ["click==8.1.3", "requests>=2.28.0"]
    updates = check_for_updates(deps)
    assert len(updates) == 2
    assert updates[0]["package"] == "click"
    assert updates[1]["package"] == "requests"

def test_up_to_date_dependencies(mock_pypi_api):
    deps = ["click==8.2.1", "werkzeug>=3.1.3"]
    updates = check_for_updates(deps)
    assert len(updates) == 0

def test_mixed_dependencies(mock_pypi_api):
    deps = ["click==8.1.3", "werkzeug==3.1.3"]
    updates = check_for_updates(deps)
    assert len(updates) == 1
    assert updates[0]["package"] == "click"

def test_no_specifier(mock_pypi_api):
    deps = ["click"]
    updates = check_for_updates(deps)
    assert len(updates) == 0

def test_non_existent_package(mock_pypi_api):
    deps = ["non-existent-package==1.0.0"]
    updates = check_for_updates(deps)
    assert len(updates) == 0 