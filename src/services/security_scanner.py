import subprocess
import json
import tempfile
import os
from packaging.requirements import Requirement
from ..utils.logging import get_logger
from .update_checker import get_latest_version

log = get_logger(__name__)

def scan_dependencies_for_vulnerabilities(dependencies: list[str]) -> list[dict]:
    """
    Scans a list of dependencies for known vulnerabilities by invoking the pip-audit CLI tool.
    If a dependency is not pinned, it resolves the latest version from PyPI before scanning.

    Args:
        dependencies: A list of dependency strings.

    Returns:
        A list of dicts, each representing a found vulnerability.
    """
    vulnerabilities = []
    
    resolved_deps = []
    log.info("Resolving dependency versions for security scan...")
    for dep_string in dependencies:
        try:
            req = Requirement(dep_string)
            # If the version is already pinned (e.g. '==1.2.3'), use it directly.
            if "==" in str(req.specifier):
                resolved_deps.append(dep_string)
            else:
                # Otherwise, find the latest version from PyPI and pin to that for the scan.
                latest_version = get_latest_version(req.name)
                if latest_version:
                    pinned_dep = f"{req.name}=={latest_version}"
                    log.info(f"Resolved unpinned dependency for scanning: '{dep_string}' -> '{pinned_dep}'")
                    resolved_deps.append(pinned_dep)
                else:
                    log.warning("Could not resolve latest version for package, skipping scan for it.", package=req.name)
        except Exception:
            # If parsing fails, it might be a simple package name without a version.
            # Try to get the latest version for it.
            latest_version = get_latest_version(dep_string)
            if latest_version:
                pinned_dep = f"{dep_string}=={latest_version}"
                log.info(f"Resolved unpinned dependency for scanning: '{dep_string}' -> '{pinned_dep}'")
                resolved_deps.append(pinned_dep)
            else:
                log.warning("Could not parse or resolve dependency, skipping", dependency=dep_string)

    if not resolved_deps:
        log.warning("No dependencies could be resolved for scanning.")
        return []

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as temp_reqs:
        temp_reqs.write("\n".join(resolved_deps))
        temp_reqs_path = temp_reqs.name
    
    try:
        # We must use 'uv run' to ensure pip-audit is in the path
        command = [
            "uv", "run", "pip-audit",
            "-r", temp_reqs_path,
            "--format", "json"
        ]
        
        # We expect a non-zero exit code if vulnerabilities are found, so we don't check for it.
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0 and result.returncode != 1:
            log.error("pip-audit command failed", stderr=result.stderr)
            return None

        if not result.stdout.strip():
            log.info("No vulnerabilities found by pip-audit.")
            return []
            
        data = json.loads(result.stdout)
        
        # Ensure we're always working with a list
        results_list = data if isinstance(data, list) else [data]

        for item in results_list:
            # The JSON output might contain non-dict items on error, so we check
            if not isinstance(item, dict):
                log.warning("Skipping unexpected item in pip-audit output", item=item)
                continue
            for vuln in item.get("vulns", []):
                vulnerabilities.append({
                    "package": item.get("name"),
                    "version": item.get("version"),
                    "id": vuln.get("id"),
                    "description": vuln.get("description"),
                    "fix_versions": vuln.get("fix_versions", []),
                })

    except json.JSONDecodeError as e:
        log.error("Failed to decode JSON from pip-audit", error=str(e), output=result.stdout)
        return None
    except Exception as e:
        log.error("An unexpected error occurred during security scan", error=str(e))
        return None
    finally:
        os.remove(temp_reqs_path)
        
    return vulnerabilities 