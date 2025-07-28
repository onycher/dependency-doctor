#!/bin/bash

# Dependency Doctor Quick Setup Script

set -e

echo "🩺 Dependency Doctor - Quick Setup"
echo "=================================="
echo

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Python version: $python_version"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

echo "✅ Project directory confirmed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -e ".[dev]"
echo "✅ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created from template"
    echo "💡 Edit .env to add your GitHub token and other settings"
else
    echo "✅ .env file already exists"
fi

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install
echo "✅ Pre-commit hooks installed"

# Run a basic test
echo "🧪 Running basic test..."
python main.py version
echo "✅ Basic functionality test passed"

echo
echo "🎉 Setup complete!"
echo
echo "Next steps:"
echo "  1. Edit .env to add your GitHub token"
echo "  2. Run 'python main.py --help' to see available commands"
echo "  3. Try 'python main.py status' to check configuration"
echo "  4. Run 'make help' to see development commands"
echo
echo "Example usage:"
echo "  python main.py deps --url https://github.com/psf/requests"
echo "  python examples/example_usage.py"
echo
echo "For development:"
echo "  source venv/bin/activate  # Activate virtual environment"
echo "  make test                 # Run tests"
echo "  make lint                 # Check code quality"
echo "  make format               # Format code"
echo