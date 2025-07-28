#!/usr/bin/env python3
"""
Example usage of Dependency Doctor

This script demonstrates how to use the Dependency Doctor programmatically
and provides examples of common use cases.
"""

import os
import sys

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.github_scanner import get_dependencies_from_github
from services.update_checker import check_for_updates
from services.security_scanner import scan_dependencies_for_vulnerabilities
from utils.config import get_config
from utils.logging import get_logger

log = get_logger(__name__)


def analyze_repository(repo_url: str, github_token: str = None):
    """
    Comprehensive analysis of a GitHub repository.
    
    Args:
        repo_url: GitHub repository URL
        github_token: Optional GitHub API token for authenticated requests
    """
    print(f"🔍 Analyzing repository: {repo_url}")
    print("=" * 60)
    
    try:
        # 1. Get dependencies
        print("📦 Fetching dependencies...")
        dependencies = get_dependencies_from_github(repo_url, token=github_token)
        
        if not dependencies:
            print("❌ No dependencies found in the repository")
            return
        
        print(f"✅ Found {len(dependencies)} dependencies:")
        for dep in dependencies:
            print(f"  • {dep}")
        print()
        
        # 2. Check for updates
        print("🔄 Checking for updates...")
        updates = check_for_updates(dependencies)
        
        if updates:
            print(f"📈 Found {len(updates)} available updates:")
            for update in updates:
                print(f"  • {update['package']}: {update['specifier']} → {update['latest_version']}")
        else:
            print("✅ All dependencies are up-to-date!")
        print()
        
        # 3. Security scan
        print("🛡️  Scanning for security vulnerabilities...")
        vulnerabilities = scan_dependencies_for_vulnerabilities(dependencies)
        
        if vulnerabilities is None:
            print("❌ Security scan failed")
        elif vulnerabilities:
            print(f"🚨 Found {len(vulnerabilities)} security vulnerabilities:")
            for vuln in vulnerabilities:
                print(f"  • {vuln['package']} {vuln['version']}: {vuln['id']}")
                print(f"    Description: {vuln['description']}")
                if vuln['fix_versions']:
                    print(f"    Fix versions: {', '.join(vuln['fix_versions'])}")
                print()
        else:
            print("✅ No security vulnerabilities found!")
            
    except Exception as e:
        log.error("Analysis failed", error=str(e))
        print(f"❌ Analysis failed: {e}")


def main():
    """Main function with example usage."""
    
    # Example repositories to analyze
    example_repos = [
        "https://github.com/psf/requests",
        "https://github.com/pallets/flask", 
        "https://github.com/django/django",
    ]
    
    # Get GitHub token from environment
    github_token = get_config("GITHUB_TOKEN")
    if not github_token:
        print("⚠️  No GitHub token found. Set GITHUB_TOKEN in .env for better rate limits")
        print()
    
    # Allow user to specify repository or use examples
    if len(sys.argv) > 1:
        repo_url = sys.argv[1]
        analyze_repository(repo_url, github_token)
    else:
        print("🩺 Dependency Doctor - Example Usage")
        print()
        print("Usage: python examples/example_usage.py [repository_url]")
        print()
        print("Example repositories:")
        for i, repo in enumerate(example_repos, 1):
            print(f"  {i}. {repo}")
        print()
        
        try:
            choice = input("Select a repository to analyze (1-3) or press Enter to skip: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(example_repos):
                repo_url = example_repos[int(choice) - 1]
                print()
                analyze_repository(repo_url, github_token)
            elif choice:
                print("Invalid choice. Exiting.")
        except KeyboardInterrupt:
            print("\nExiting...")


if __name__ == "__main__":
    main()