import requests
from packaging.version import parse as parse_version
from packaging.requirements import Requirement
from ..utils.logging import get_logger

log = get_logger(__name__)


def get_latest_version(package_name: str) -> str | None:
    """
    Gets the latest version of a package from PyPI.

    Args:
        package_name: The name of the package.

    Returns:
        The latest version string, or None if not found.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["info"]["version"]
    except requests.RequestException as e:
        log.error("Failed to fetch from PyPI", package=package_name, error=str(e))
        return None
    except KeyError:
        log.error("Unexpected PyPI response format", package=package_name)
        return None


def check_for_updates(dependencies: list[str]) -> list[dict]:
    """
    For a list of dependencies, finds and compares versions to identify outdated packages.

    Args:
        dependencies: A list of dependency strings.

    Returns:
        A list of dicts with actionable update information.
    """
    updates = []
    for dep_string in dependencies:
        try:
            req = Requirement(dep_string)
            package_name = req.name

            if req.url:
                continue

            latest_version_str = get_latest_version(package_name)

            if not latest_version_str:
                continue

            # If there is no version specifier, we cannot determine if it's outdated.
            if not req.specifier:
                continue

            # Heuristic: Extract the version from the first specifier in the set.
            # This handles cases like '>=', '==', and '~=' by comparing against the base version.
            specified_version_str = list(req.specifier)[0].version

            # Only report if the latest version is strictly newer than the specified one.
            if parse_version(latest_version_str) > parse_version(specified_version_str):
                updates.append({
                    "package": package_name,
                    "specifier": str(req.specifier),
                    "latest_version": latest_version_str,
                })
        except Exception as e:
            log.warning(
                "Could not parse or check dependency",
                dep_string=dep_string,
                error=str(e),
            )
            continue
    return updates 