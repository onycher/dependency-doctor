import pytest
from unittest.mock import patch, MagicMock
import json
from src.services.security_scanner import scan_dependencies_for_vulnerabilities

# Mock data for pip-audit subprocess call
VULNERABLE_PKG_JSON = json.dumps([
    {
        "name": "vulnerable-package",
        "version": "1.0.0",
        "vulns": [
            {
                "id": "PYSEC-2023-123",
                "description": "A critical vulnerability.",
                "fix_versions": ["1.0.1", "1.1.0"]
            }
        ]
    }
])

NO_VULNS_JSON = json.dumps([])

@patch('src.services.security_scanner.subprocess.run')
@patch('src.services.security_scanner.get_latest_version')
def test_scan_with_unpinned_dependency_and_vulnerability(mock_get_latest, mock_subprocess_run):
    """
    Test scanning an unpinned dependency that resolves to a vulnerable version.
    """
    # Arrange
    mock_get_latest.return_value = "1.0.0"
    mock_subprocess_run.return_value = MagicMock(
        returncode=1, # pip-audit returns 1 when vulnerabilities are found
        stdout=VULNERABLE_PKG_JSON,
        stderr=""
    )
    
    # Act
    vulnerabilities = scan_dependencies_for_vulnerabilities(["vulnerable-package>=0.9.0"])
    
    # Assert
    assert len(vulnerabilities) == 1
    assert vulnerabilities[0]['package'] == 'vulnerable-package'
    assert vulnerabilities[0]['id'] == 'PYSEC-2023-123'
    mock_get_latest.assert_called_once_with('vulnerable-package')


@patch('src.services.security_scanner.subprocess.run')
@patch('src.services.security_scanner.get_latest_version')
def test_scan_with_pinned_dependency_no_vulnerability(mock_get_latest, mock_subprocess_run):
    """
    Test scanning a pinned dependency that has no vulnerabilities.
    """
    # Arrange
    mock_subprocess_run.return_value = MagicMock(
        returncode=0,
        stdout=NO_VULNS_JSON,
        stderr=""
    )
    
    # Act
    vulnerabilities = scan_dependencies_for_vulnerabilities(["clean-package==1.2.3"])
    
    # Assert
    assert len(vulnerabilities) == 0
    mock_get_latest.assert_not_called() # Should not be called for pinned deps


@patch('src.services.security_scanner.subprocess.run')
def test_scan_subprocess_fails(mock_subprocess_run):
    """
    Test that the function returns None when the pip-audit command fails.
    """
    # Arrange
    mock_subprocess_run.return_value = MagicMock(
        returncode=2, # A code other than 0 or 1 indicates an error
        stdout="",
        stderr="pip-audit error"
    )
    
    # Act
    result = scan_dependencies_for_vulnerabilities(["any-package==1.0.0"])
    
    # Assert
    assert result is None

@patch('src.services.security_scanner.subprocess.run')
def test_scan_json_decode_error(mock_subprocess_run):
    """
    Test that the function returns None when pip-audit returns malformed JSON.
    """
    # Arrange
    mock_subprocess_run.return_value = MagicMock(
        returncode=1,
        stdout="this is not json",
        stderr=""
    )
    
    # Act
    result = scan_dependencies_for_vulnerabilities(["any-package==1.0.0"])
    
    # Assert
    assert result is None


def test_scan_with_no_dependencies():
    """
    Test that the function returns an empty list when given no dependencies.
    """
    # Act
    result = scan_dependencies_for_vulnerabilities([])
    
    # Assert
    assert result == []

@patch('src.services.security_scanner.get_latest_version')
def test_scan_unable_to_resolve_dependency(mock_get_latest):
    """
    Test that an unresolvable dependency is skipped and does not cause a crash.
    """
    # Arrange
    mock_get_latest.return_value = None # Simulate PyPI not finding the package
    
    # Act
    result = scan_dependencies_for_vulnerabilities(["non-existent-package"])
    
    # Assert
    assert result == []
    mock_get_latest.assert_called_once_with('non-existent-package') 