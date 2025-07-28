#!/usr/bin/env python3
"""
Basic dependency analyzer that works without external dependencies.
This provides core functionality for analyzing repository structure.
"""

import os
import json
import urllib.request
import urllib.parse
import re
from typing import List, Dict, Optional


def analyze_github_repo_basic(repo_url: str) -> Dict:
    """
    Basic GitHub repository analysis using only standard library.
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Dict with analysis results
    """
    # Parse repository URL
    parsed = urllib.parse.urlparse(repo_url)
    path_parts = parsed.path.strip('/').split('/')
    
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub URL format")
    
    owner, repo = path_parts[0], path_parts[1]
    
    # Basic repo info
    result = {
        'owner': owner,
        'repo': repo,
        'url': repo_url,
        'dependencies': [],
        'dependency_files': [],
        'analysis': {}
    }
    
    # Try to fetch repository info via GitHub API (public, no auth)
    try:
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        with urllib.request.urlopen(api_url) as response:
            repo_data = json.loads(response.read().decode())
            result['analysis']['stars'] = repo_data.get('stargazers_count', 0)
            result['analysis']['language'] = repo_data.get('language', 'Unknown')
            result['analysis']['description'] = repo_data.get('description', '')
    except Exception as e:
        result['analysis']['error'] = f"Could not fetch repo info: {e}"
    
    # Try to fetch common dependency files
    files_to_check = [
        'pyproject.toml',
        'requirements.txt',
        'setup.py',
        'Pipfile',
        'poetry.lock'
    ]
    
    for filename in files_to_check:
        try:
            file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{filename}"
            with urllib.request.urlopen(file_url) as response:
                content = response.read().decode()
                result['dependency_files'].append({
                    'filename': filename,
                    'size': len(content),
                    'lines': len(content.splitlines())
                })
                
                # Basic dependency extraction
                if filename == 'requirements.txt':
                    deps = extract_requirements_txt(content)
                    result['dependencies'].extend(deps)
                
        except Exception:
            # File doesn't exist or couldn't be fetched
            pass
    
    return result


def extract_requirements_txt(content: str) -> List[str]:
    """Extract dependencies from requirements.txt content."""
    dependencies = []
    
    for line in content.splitlines():
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
            
        # Skip pip options
        if line.startswith('-'):
            continue
            
        # Basic dependency extraction (package name)
        # This is a simplified parser
        match = re.match(r'^([a-zA-Z0-9\-_.]+)', line)
        if match:
            dependencies.append(line)
    
    return dependencies


def generate_basic_report(analysis: Dict) -> None:
    """Generate a basic text report from analysis."""
    print(f"📊 Repository Analysis: {analysis['repo']}")
    print("=" * 60)
    print(f"Owner: {analysis['owner']}")
    print(f"Repository: {analysis['repo']}")
    print(f"URL: {analysis['url']}")
    
    if 'language' in analysis['analysis']:
        print(f"Language: {analysis['analysis']['language']}")
    if 'stars' in analysis['analysis']:
        print(f"Stars: {analysis['analysis']['stars']}")
    if 'description' in analysis['analysis']:
        print(f"Description: {analysis['analysis']['description']}")
    
    print(f"\n📁 Dependency Files Found: {len(analysis['dependency_files'])}")
    for file_info in analysis['dependency_files']:
        print(f"  • {file_info['filename']} ({file_info['lines']} lines)")
    
    print(f"\n📦 Dependencies Found: {len(analysis['dependencies'])}")
    for i, dep in enumerate(analysis['dependencies'][:10], 1):  # Show first 10
        print(f"  {i:2d}. {dep}")
    
    if len(analysis['dependencies']) > 10:
        print(f"  ... and {len(analysis['dependencies']) - 10} more")
    
    if not analysis['dependencies']:
        print("  No dependencies detected in requirements.txt")
        print("  Note: This basic analyzer only supports requirements.txt")


def main():
    """Main function for standalone usage."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python basic_analyzer.py <github_repo_url>")
        print("Example: python basic_analyzer.py https://github.com/psf/requests")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    
    try:
        analysis = analyze_github_repo_basic(repo_url)
        generate_basic_report(analysis)
    except Exception as e:
        print(f"❌ Error analyzing repository: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()