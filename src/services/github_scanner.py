import os
import tempfile
import requests
import zipfile
import tomllib
from github import Github, UnknownObjectException
import base64
import re
from src.utils.logging import get_logger

log = get_logger(__name__)

GITHUB_ZIP_URL = "https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"

GITHUB_URL_RE = re.compile(r"github.com/([^/]+)/([^/]+?)(?:\.git)?(?:/|$)")

COMMON_DEP_KEYS = [
    ("project", "dependencies"),  # PEP 621
    ("tool", "poetry", "dependencies"),  # Poetry
    ("tool", "flit", "metadata", "requires"),  # Flit
]

def download_and_extract_github_repo(url, branch="main"):
    """
    Download a GitHub repo as a zip and extract it to a temp directory.
    Returns the path to the extracted directory.
    """
    # Parse owner and repo from URL
    try:
        parts = url.rstrip('/').split('/')
        owner, repo = parts[-2], parts[-1]
    except Exception:
        raise ValueError("Invalid GitHub URL format")
    zip_url = GITHUB_ZIP_URL.format(owner=owner, repo=repo, branch=branch)
    response = requests.get(zip_url)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to download repo zip: {zip_url}")
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"{repo}.zip")
    with open(zip_path, "wb") as f:
        f.write(response.content)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)
    # The extracted folder is usually {repo}-{branch}
    extracted_dir = os.path.join(temp_dir, f"{repo}-{branch}")
    return extracted_dir, temp_dir

def get_dependencies_from_github(url, branch="main", token=None):
    """
    Fetch dependencies from a GitHub repo, checking pyproject.toml first, then requirements.txt.
    """
    m = GITHUB_URL_RE.search(url)
    if not m:
        log.error("Invalid GitHub URL format", url=url)
        raise ValueError(f"Invalid GitHub URL format: {url}")
    owner, repo = m.group(1), m.group(2)
    log.info("Parsed GitHub repo info", owner=owner, repo=repo)

    try:
        gh = Github(token) if token else Github()
        repo_obj = gh.get_repo(f"{owner}/{repo}")
    except UnknownObjectException:
        log.error("GitHub repository not found or access denied.", owner=owner, repo=repo)
        raise  # Re-raise to be caught by the CLI
    except Exception as e:
        log.error("Failed to connect to GitHub", error=str(e))
        raise

    # Try pyproject.toml first
    try:
        file_content = repo_obj.get_contents("pyproject.toml", ref=branch)
        content = base64.b64decode(file_content.content).decode()
        pyproject = tomllib.loads(content)
        for key_path in COMMON_DEP_KEYS:
            d = pyproject
            for key in key_path:
                if not isinstance(d, dict):
                    d = None
                    break
                if key in d:
                    d = d[key]
                else:
                    d = None
                    break
            if d:
                if isinstance(d, dict):
                    return [k for k in d.keys() if k != "python"]
                if isinstance(d, list):
                    return d
    except UnknownObjectException:
        log.info("pyproject.toml not found, falling back to requirements.txt")
    except Exception as e:
        log.warning("Failed to parse pyproject.toml, falling back to requirements.txt", error=str(e))

    # Fallback to requirements.txt
    try:
        file_content = repo_obj.get_contents("requirements.txt", ref=branch)
        content = base64.b64decode(file_content.content).decode()
        return [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
    except UnknownObjectException:
        log.info("No dependency files (pyproject.toml or requirements.txt) found in the repository.")
        return []
    except Exception as e:
        log.error("Failed to read or parse requirements.txt from GitHub", error=str(e))
        return [] 