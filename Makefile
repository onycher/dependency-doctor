.PHONY: help install test lint format clean build docker-build docker-run

# Default target
help:
	@echo "🩺 Dependency Doctor - Development Commands"
	@echo "============================================"
	@echo "install    - Install dependencies in development mode"
	@echo "test       - Run tests"
	@echo "lint       - Run linting checks"
	@echo "format     - Format code"
	@echo "clean      - Clean build artifacts"
	@echo "build      - Build package"
	@echo "docker-build - Build Docker image"
	@echo "docker-run   - Run in Docker container"
	@echo "example    - Run example analysis"

# Development setup
install:
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest tests/ -v --cov=src

test-fast:
	pytest tests/ -x

# Code quality
lint:
	ruff check src/ tests/
	mypy src/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

# Build
build: clean
	python -m build

# Docker
docker-build:
	docker build -t dependency-doctor .

docker-run: docker-build
	docker run --rm -it dependency-doctor

docker-web: docker-build
	docker run --rm -p 8000:8000 dependency-doctor python main.py --mode web

docker-api: docker-build
	docker run --rm -p 8001:8001 dependency-doctor python main.py --mode api

# Examples
example:
	python examples/example_usage.py

example-basic:
	python src/utils/basic_analyzer.py https://github.com/psf/requests

# Development server
dev-web:
	python main.py --mode web

dev-api:
	python main.py --mode api

# CLI examples
cli-status:
	python main.py status

cli-version:
	python main.py version

# Security
security-scan:
	pip-audit --desc --format=json

# Documentation
docs:
	@echo "📚 Opening documentation..."
	@echo "README: file://$(PWD)/README.md"
	@echo "Contributing: file://$(PWD)/CONTRIBUTING.md"