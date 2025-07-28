# 🩺 Dependency Doctor

A comprehensive tool for analyzing, monitoring, and managing Python project dependencies with security scanning, update checking, and intelligent recommendations.

## ✨ Features

- 📊 **Dependency Analysis**: Scan GitHub repositories for dependencies from `pyproject.toml` and `requirements.txt`
- 🔍 **Update Checking**: Identify outdated packages with intelligent version comparison
- 🛡️ **Security Scanning**: Detect vulnerabilities in your dependencies
- 🖥️ **Multiple Interfaces**: CLI, Web UI, and REST API
- 📈 **Rich Output**: Beautiful tables and formatted reports
- 🔧 **Flexible Configuration**: Environment-based configuration with `.env` support

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/onycher/dependency-doctor.git
cd dependency-doctor

# Install dependencies
pip install -e .

# Optional: Set up environment variables
cp .env.example .env
# Edit .env with your GitHub token and other settings
```

### Basic Usage

```bash
# Check tool status
python -m src.controllers.cli_controller status

# Scan a GitHub repository for dependencies
python -m src.controllers.cli_controller deps --url https://github.com/user/repo

# Check for outdated dependencies
python -m src.controllers.cli_controller check-updates --url https://github.com/user/repo

# Security scan for vulnerabilities
python -m src.controllers.cli_controller security-scan --url https://github.com/user/repo
```

## 📋 Commands

### CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `status` | Show tool version and configuration | `dependency-doctor status` |
| `deps` | List direct dependencies from a repository | `dependency-doctor deps --url <repo-url>` |
| `check-updates` | Find outdated dependencies | `dependency-doctor check-updates --url <repo-url>` |
| `security-scan` | Scan for security vulnerabilities | `dependency-doctor security-scan --url <repo-url>` |

### Web Interface

Start the web interface:

```bash
python -m src.web.dashboard
```

Access the dashboard at `http://localhost:8000` for a user-friendly interface.

### API Endpoints

Start the API server:

```bash
python -m src.controllers.api_controller
```

Available endpoints:
- `GET /status` - Service health check
- `POST /dependencies` - Analyze repository dependencies
- `POST /security` - Security vulnerability scan

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# GitHub API token for authenticated requests (recommended)
GITHUB_TOKEN=your_github_token_here

# API configuration
API_KEY=your_api_key_here

# Debug mode
DEBUG=false
```

### GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `public_repo` scope
3. Add it to your `.env` file as `GITHUB_TOKEN`

## 🏗️ Architecture

```
src/
├── controllers/          # Interface controllers
│   ├── cli_controller.py    # Command-line interface
│   ├── api_controller.py    # REST API endpoints
│   └── web_controller.py    # Web UI controller
├── services/             # Core business logic
│   ├── github_scanner.py    # Repository scanning
│   ├── update_checker.py    # Version comparison
│   └── security_scanner.py  # Vulnerability detection
├── utils/                # Utilities
│   ├── config.py            # Configuration management
│   └── logging.py           # Structured logging
└── web/                  # Web interface
    └── dashboard.py         # Rio-based UI
```

## 🔧 Development

### Prerequisites

- Python 3.12+
- Git

### Setup Development Environment

```bash
# Clone and install in development mode
git clone https://github.com/onycher/dependency-doctor.git
cd dependency-doctor
pip install -e .

# Run tests
pytest tests/

# Code formatting and linting
ruff check src/ tests/
ruff format src/ tests/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_github_scanner.py -v
```

## 📊 Example Output

### Dependency List
```
Direct dependencies:
  - click>=8.2.1
  - fastapi>=0.116.1
  - pytest>=8.4.1
  - structlog>=25.4.0
```

### Update Check
```
Available updates:
  - click: Specified: >=8.2.1, Latest: 8.3.0
  - pytest: Specified: >=8.4.1, Latest: 8.5.2
```

### Security Scan
```
🚨 Found 2 vulnerabilities:
┌─────────┬─────────┬──────────┬──────────────┬─────────────────────┐
│ Package │ Version │ ID       │ Fix Versions │ Description         │
├─────────┼─────────┼──────────┼──────────────┼─────────────────────┤
│ urllib3 │ 1.26.0  │ CVE-2021 │ 1.26.5+     │ HTTPS proxy issue   │
└─────────┴─────────┴──────────┴──────────────┴─────────────────────┘
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Issues](https://github.com/onycher/dependency-doctor/issues)
- [Pull Requests](https://github.com/onycher/dependency-doctor/pulls)
- [Discussions](https://github.com/onycher/dependency-doctor/discussions)

## 🙏 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- [FastAPI](https://fastapi.tiangolo.com/) for REST API
- [Rio UI](https://rio.dev/) for web interface
- [structlog](https://structlog.org/) for structured logging

---

⭐ Star this repository if you find it helpful!