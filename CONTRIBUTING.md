# Contributing to Dependency Doctor

Thank you for your interest in contributing to Dependency Doctor! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/dependency-doctor.git
   cd dependency-doctor
   ```
3. **Install** dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. **Create** a branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📋 Development Guidelines

### Code Style

We use several tools to maintain code quality:

- **Ruff** for linting and formatting
- **MyPy** for type checking
- **Pytest** for testing

Run quality checks:
```bash
# Format code
ruff format src/ tests/

# Check for linting issues
ruff check src/ tests/

# Type checking
mypy src/

# Run tests
pytest tests/
```

### Commit Guidelines

We follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(cli): add dependency visualization command
fix(scanner): handle private repositories correctly
docs(readme): update installation instructions
test(services): add tests for security scanner
```

### Testing

- Write tests for all new functionality
- Ensure existing tests pass
- Aim for good test coverage
- Use descriptive test names

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_github_scanner.py -v
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions and classes
- Update TODO.md for implementation progress
- Include examples in docstrings when helpful

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Environment information** (Python version, OS, dependencies)
2. **Steps to reproduce** the issue
3. **Expected behavior**
4. **Actual behavior**
5. **Error messages** or logs (if any)
6. **Minimal example** demonstrating the issue

Use our issue templates when available.

## 💡 Suggesting Features

Before suggesting a new feature:

1. Check if it already exists in the TODO.md
2. Search existing issues and discussions
3. Consider if it fits the project's scope and goals

For feature requests, please include:
- **Use case** - why is this feature needed?
- **Proposed solution** - how should it work?
- **Alternatives considered**
- **Additional context**

## 🏗️ Development Setup

### Environment Setup

1. **Python 3.12+** is required
2. **Git** for version control
3. **Virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

### Project Structure

```
dependency-doctor/
├── src/                    # Main source code
│   ├── controllers/        # Interface controllers (CLI, API, Web)
│   ├── services/          # Core business logic
│   ├── utils/             # Utility functions
│   └── web/               # Web interface components
├── tests/                 # Test suite
├── docs/                  # Documentation
├── pyproject.toml         # Project configuration
├── README.md              # Project overview
└── TODO.md                # Implementation roadmap
```

### Key Components

- **CLI Controller**: Click-based command line interface
- **GitHub Scanner**: Repository dependency analysis
- **Update Checker**: Version comparison and update detection
- **Security Scanner**: Vulnerability detection
- **Web Dashboard**: Rio-based web interface
- **API Controller**: FastAPI-based REST API

## 🔍 Code Review Process

1. **Self-review** your changes before submitting
2. **Run all tests** and quality checks
3. **Update documentation** as needed
4. **Submit a pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots for UI changes
   - Breaking changes noted

### Pull Request Guidelines

- Keep PRs focused and reasonably sized
- Include tests for new functionality
- Update documentation for user-facing changes
- Follow the existing code style
- Write clear commit messages

## 🤝 Community

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow our Code of Conduct

## ❓ Getting Help

If you need help:

1. Check the documentation and README
2. Search existing issues and discussions
3. Ask questions in GitHub Discussions
4. Join the conversation in issues

## 📝 License

By contributing to Dependency Doctor, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Special thanks in documentation

Thank you for contributing to Dependency Doctor! 🎉