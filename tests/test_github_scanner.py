import pytest
from unittest.mock import patch
from src.services.github_scanner import get_dependencies_from_github
from github import GithubException

FLASK_PYPROJECT_TOML = '''
[project]
name = "Flask"
dependencies = [
    "blinker>=1.9.0",
    "click>=8.1.3",
]
'''

BLACK_REQUIREMENTS_TXT = '''
click>=8.0.0
# a comment
mypy_extensions>=0.4.3

pathspec>=0.9.0
'''

class DummyFileContent:
    def __init__(self, content):
        import base64
        self.content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

class MockGithubRepo:
    def __init__(self, files):
        self._files = files

    def get_contents(self, path, ref=None):
        if path in self._files:
            return DummyFileContent(self._files[path])
        raise GithubException(404, "Not Found", headers=None)

@patch("src.services.github_scanner.Github")
def test_get_dependencies_pyproject_first(mock_github):
    mock_repo = MockGithubRepo({
        "pyproject.toml": FLASK_PYPROJECT_TOML,
        "requirements.txt": BLACK_REQUIREMENTS_TXT  # Should not be used
    })
    mock_github.return_value.get_repo.return_value = mock_repo
    deps = get_dependencies_from_github("https://github.com/pallets/flask")
    assert "blinker>=1.9.0" in deps
    assert "click>=8.1.3" in deps
    assert len(deps) == 2

@patch("src.services.github_scanner.Github")
def test_get_dependencies_requirements_fallback(mock_github):
    mock_repo = MockGithubRepo({"requirements.txt": BLACK_REQUIREMENTS_TXT})
    mock_github.return_value.get_repo.return_value = mock_repo
    deps = get_dependencies_from_github("https://github.com/psf/black")
    assert "click>=8.0.0" in deps
    assert "mypy_extensions>=0.4.3" in deps
    assert "pathspec>=0.9.0" in deps
    assert len(deps) == 3

@patch("src.services.github_scanner.Github")
def test_get_dependencies_no_files_found(mock_github):
    mock_repo = MockGithubRepo({})
    mock_github.return_value.get_repo.return_value = mock_repo
    deps = get_dependencies_from_github("https://github.com/user/repo")
    assert deps == [] 