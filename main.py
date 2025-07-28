#!/usr/bin/env python3
"""
Dependency Doctor - Main entry point

This script provides multiple ways to start Dependency Doctor:
- CLI interface (default)
- Web UI 
- API server
"""

import sys
import argparse
from src.controllers.cli_controller import cli


def main():
    """Main entry point for Dependency Doctor."""
    parser = argparse.ArgumentParser(
        description="Dependency Doctor - Analyze and manage Python dependencies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start CLI (default)
  python main.py --mode cli         # Start CLI explicitly  
  python main.py --mode web         # Start web interface
  python main.py --mode api         # Start API server
  
For CLI commands, use:
  python main.py status
  python main.py deps --url <repo-url>
  python main.py check-updates --url <repo-url>
  python main.py security-scan --url <repo-url>
        """
    )
    
    parser.add_argument(
        "--mode", 
        choices=["cli", "web", "api"], 
        default="cli",
        help="Interface mode to start (default: cli)"
    )
    
    # Parse known args to handle CLI commands
    args, unknown = parser.parse_known_args()
    
    if args.mode == "web":
        try:
            from src.web.dashboard import main as web_main
            print("🚀 Starting Dependency Doctor Web Interface...")
            web_main()
        except ImportError as e:
            print(f"❌ Error: Web interface dependencies not available: {e}")
            print("Install with: pip install -e '.[dev]'")
            sys.exit(1)
    
    elif args.mode == "api":
        try:
            from src.controllers.api_controller import main as api_main
            print("🚀 Starting Dependency Doctor API Server...")
            api_main()
        except ImportError as e:
            print(f"❌ Error: API server dependencies not available: {e}")
            print("Install with: pip install -e '.[dev]'")
            sys.exit(1)
    
    else:  # CLI mode (default)
        # Restore original sys.argv for Click to handle CLI commands
        if unknown:
            sys.argv = [sys.argv[0]] + unknown
        else:
            # If no additional args, show help
            if len(sys.argv) == 1 or (len(sys.argv) == 3 and "--mode" in sys.argv):
                print("🩺 Dependency Doctor CLI")
                print("Use --help for available commands")
                print("\nQuick examples:")
                print("  python main.py status")
                print("  python main.py deps --url https://github.com/user/repo")
                print("  python main.py check-updates --url https://github.com/user/repo")
                return
        
        try:
            cli()
        except Exception as e:
            print(f"❌ Error running CLI: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
