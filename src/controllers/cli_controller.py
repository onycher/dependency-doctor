from src.utils.logging import get_logger
from src.utils.config import get_config
import os
import sys

# Handle optional dependencies gracefully
try:
    import click
except ImportError:
    print("Error: Click library is required but not installed.")
    print("Install with: pip install click")
    sys.exit(1)

try:
    import toml
except ImportError:
    print("Error: toml library is required but not installed.")
    print("Install with: pip install toml")
    sys.exit(1)

# Import services with error handling
try:
    from src.services.github_scanner import get_dependencies_from_github
    from src.services.update_checker import check_for_updates
    from src.services.security_scanner import scan_dependencies_for_vulnerabilities
except ImportError as e:
    print(f"Error importing services: {e}")
    print("Please ensure all dependencies are installed.")

# Optional rich/prettytable imports
try:
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from prettytable import PrettyTable
    PRETTYTABLE_AVAILABLE = True
except ImportError:
    PRETTYTABLE_AVAILABLE = False

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
            print("No dependencies found to scan.")
            return

        print("Scanning for vulnerabilities...")
        vulnerabilities = scan_dependencies_for_vulnerabilities(dependencies)

        if vulnerabilities is None:
            log.error("The security scan failed to complete.")
            print("Error: The security scan could not be completed. Check the logs for details.")
            return

        if not vulnerabilities:
            print("✅ No vulnerabilities found.")
            log.info("✅ No vulnerabilities found.")
            return

        print(f"🚨 Found {len(vulnerabilities)} vulnerabilities:")
        log.info(f"🚨 Found {len(vulnerabilities)} vulnerabilities.")
        
        # Use prettytable if available, otherwise use simple formatting
        if PRETTYTABLE_AVAILABLE:
            table = PrettyTable()
            table.field_names = ["Package", "Version", "ID", "Fix Versions", "Description"]
            table.align = "l"
            for vuln in vulnerabilities:
                table.add_row([
                    vuln['package'], 
                    vuln['version'], 
                    vuln['id'], 
                    ', '.join(vuln['fix_versions']),
                    vuln['description'][:50] + "..." if len(vuln['description']) > 50 else vuln['description']
                ])
            print(table)
        else:
            # Fallback to simple text formatting
            for i, vuln in enumerate(vulnerabilities, 1):
                print(f"\n{i}. {vuln['package']} {vuln['version']}")
                print(f"   ID: {vuln['id']}")
                print(f"   Description: {vuln['description']}")
                if vuln['fix_versions']:
                    print(f"   Fix versions: {', '.join(vuln['fix_versions'])}")

    except Exception as e:
        log.error("Failed during security scan", error=str(e))
        print(f"An error occurred: {e}")


@cli.command()
@click.option('--url', required=True, help='GitHub repository URL to analyze')
def info(url):
    """Show detailed information about a GitHub repository's dependency structure."""
    log.info("info command called", url=url)
    print(f"📊 Repository Information: {url}")
    print("=" * 60)
    
    try:
        token = get_config("GITHUB_TOKEN")
        if not token:
            print("⚠️  Note: No GitHub token found. Rate limits may apply.")
            print("   Set GITHUB_TOKEN in .env for better performance.\n")
        
        # Basic repository info
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            owner, repo = path_parts[0], path_parts[1]
            print(f"Owner: {owner}")
            print(f"Repository: {repo}")
            print(f"URL: {url}\n")
        
        print("🔍 Analyzing dependency files...")
        deps = get_dependencies_from_github(url, token=token)
        
        if not deps:
            print("❌ No dependency files found (pyproject.toml, requirements.txt)")
            print("\nTip: Ensure the repository contains one of these files:")
            print("  • pyproject.toml (PEP 621 format)")
            print("  • requirements.txt")
            return
        
        print(f"✅ Found {len(deps)} dependencies")
        print("\n📦 Dependencies:")
        for i, dep in enumerate(deps, 1):
            print(f"  {i:2d}. {dep}")
        
        # Additional analysis
        print(f"\n📈 Quick Statistics:")
        print(f"  • Total dependencies: {len(deps)}")
        
        # Count by type (very basic heuristic)
        dev_keywords = ['test', 'dev', 'debug', 'lint', 'format', 'mypy', 'pytest', 'black', 'ruff']
        dev_deps = [d for d in deps if any(keyword in d.lower() for keyword in dev_keywords)]
        prod_deps = len(deps) - len(dev_deps)
        
        print(f"  • Likely production deps: {prod_deps}")
        print(f"  • Likely development deps: {len(dev_deps)}")
        
        print(f"\n💡 Next Steps:")
        print(f"  • Run 'check-updates --url {url}' to find outdated packages")
        print(f"  • Run 'security-scan --url {url}' to check for vulnerabilities")
        
    except Exception as e:
        log.error("Failed to get repository info", error=str(e))
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  • Check that the repository URL is correct and public")
        print("  • Verify your internet connection")
        print("  • Set GITHUB_TOKEN for private repositories")


@cli.command()
def version():
    """Show Dependency Doctor version and system information."""
    print("🩺 Dependency Doctor")
    print(f"Version: {get_version()}")
    print(f"Python: {sys.version}")
    print(f"Platform: {os.name}")
    
    # Check for optional dependencies
    print("\n📦 Optional Dependencies:")
    optional_deps = [
        ('structlog', 'Enhanced logging'),
        ('python-dotenv', '.env file support'),
        ('rich', 'Rich console output'),
        ('prettytable', 'Table formatting'),
        ('PyGithub', 'GitHub API access'),
        ('packaging', 'Version parsing'),
        ('requests', 'HTTP requests'),
    ]
    
    for dep, description in optional_deps:
        try:
            __import__(dep.replace('-', '_'))
            status = "✅ Available"
        except ImportError:
            status = "❌ Missing"
        print(f"  • {dep:<15} ({description:<20}): {status}")


if __name__ == '__main__':
    cli() 