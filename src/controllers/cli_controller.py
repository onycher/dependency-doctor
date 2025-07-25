from src.utils.logging import get_logger
from src.utils.config import get_config
import click
import os
import toml
from src.services.github_scanner import get_dependencies_from_github
from src.services.update_checker import check_for_updates
from src.services.security_scanner import scan_dependencies_for_vulnerabilities
from rich.console import Console
from rich.table import Table
from prettytable import PrettyTable

log = get_logger(__name__)

def get_version():
    try:
        pyproject = toml.load("pyproject.toml")
        return pyproject["project"]["version"]
    except Exception as e:
        log.error("Failed to read version from pyproject.toml", error=str(e))
        return "unknown"

@click.group()
def cli():
    """Dependency Doctor CLI"""
    log.info("CLI started")
    pass

@cli.command()
def status():
    """Show Dependency Doctor status, environment config, and version."""
    log.info("doctor status command called")
    print("Dependency Doctor CLI is working!")
    print(f"Version: {get_version()}")
    print("Environment Config:")
    for key in ["DEBUG", "API_KEY"]:
        value = get_config(key)
        print(f"  {key}: {value}")
    print(f"Python executable: {os.sys.executable}")
    print(f"Current working directory: {os.getcwd()}")

@cli.command()
@click.option('--url', required=True, help='GitHub repository URL to scan')
def deps(url):
    """List direct dependencies from a GitHub repository."""
    log.info("doctor deps command called", url=url)
    try:
        token = get_config("GITHUB_TOKEN")
        deps = get_dependencies_from_github(url, token=token)
        if not deps:
            print("No direct dependencies found in pyproject.toml or requirements.txt.")
        else:
            print("Direct dependencies:")
            for dep in deps:
                print(f"  - {dep}")
    except Exception as e:
        log.error("Failed to fetch dependencies from GitHub", error=str(e))
        print(f"Error: {e}")

@cli.command(name="check-updates")
@click.option('--url', required=True, help='The URL of the GitHub repository to check.')
def check_updates(url):
    """Check for outdated dependencies in a GitHub repository."""
    log.info("check-updates command called", url=url)
    try:
        token = get_config("GITHUB_TOKEN")
        deps = get_dependencies_from_github(url, token=token)
        if not deps:
            print("No dependencies found to check.")
            return

        print("Checking for updates...")
        updates = check_for_updates(deps)

        if not updates:
            print("All dependencies are up-to-date!")
            return

        print("Available updates:")
        for update in updates:
            print(
                f"  - {update['package']}: "
                f"Specified: {update['specifier']}, "
                f"Latest: {update['latest_version']}"
            )
    except Exception as e:
        log.error("Failed during update check", error=str(e))
        print(f"An error occurred: {e}")


@cli.command(name="security-scan")
@click.option('--url', required=True, help='The URL of the GitHub repository to scan.')
def security_scan(url):
    """Scans the dependencies of a GitHub repository for known vulnerabilities."""
    log.info("security-scan command called", url=url)
    try:
        github_token = get_config("GITHUB_TOKEN")
        dependencies = get_dependencies_from_github(url, token=github_token)
        if not dependencies:
            log.warning("No dependencies found to scan.")
            return

        vulnerabilities = scan_dependencies_for_vulnerabilities(dependencies)

        if vulnerabilities is None:
            log.error("The security scan failed to complete.")
            print("Error: The security scan could not be completed. Check the logs for details.")
            return

        if not vulnerabilities:
            log.info("✅ No vulnerabilities found.")
            return

        log.info(f"🚨 Found {len(vulnerabilities)} vulnerabilities.")
        table = PrettyTable()
        table.field_names = ["Package", "Version", "ID", "Fix Versions", "Description"]
        table.align = "l"
        for vuln in vulnerabilities:
            table.add_row([
                vuln['package'], 
                vuln['version'], 
                vuln['id'], 
                ', '.join(vuln['fix_versions']),
                vuln['description']
            ])
        print(table)

    except Exception as e:
        log.error("Failed during security scan", error=str(e))
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    cli() 