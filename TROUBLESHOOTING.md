# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### 1. "Module not found" errors
**Problem**: Import errors when running the application
```
ModuleNotFoundError: No module named 'structlog'
```

**Solutions**:
- Install dependencies: `pip install -e .`
- Use virtual environment: `python -m venv venv && source venv/bin/activate`
- Run the quick setup: `./setup.sh`

#### 2. Network timeouts during installation
**Problem**: Pip install fails with timeout errors
```
ReadTimeoutError: HTTPSConnectionPool(host='pypi.org', port=443): Read timed out.
```

**Solutions**:
- Increase timeout: `pip install --timeout 300 -e .`
- Use different index: `pip install -i https://pypi.python.org/simple/ -e .`
- Install minimal dependencies first: `pip install click toml`

### Configuration Issues

#### 3. GitHub API rate limiting
**Problem**: "API rate limit exceeded" errors

**Solutions**:
- Get a GitHub token: https://github.com/settings/tokens
- Add to `.env`: `GITHUB_TOKEN=your_token_here`
- Use authenticated requests for higher rate limits

#### 4. Environment variables not loading
**Problem**: Configuration values not found

**Solutions**:
- Create `.env` file: `cp .env.example .env`
- Set environment variables manually: `export GITHUB_TOKEN=your_token`
- Check file location: `.env` should be in project root

### Runtime Issues

#### 5. "Repository not found" errors
**Problem**: Cannot access GitHub repository

**Solutions**:
- Check repository URL format: `https://github.com/owner/repo`
- Verify repository is public or token has access
- Check internet connectivity

#### 6. Security scan failures
**Problem**: pip-audit not working

**Solutions**:
- Install pip-audit: `pip install pip-audit`
- Check if dependencies are properly formatted
- Use fallback mode if available

### Development Issues

#### 7. Pre-commit hooks failing
**Problem**: Git commits rejected by pre-commit

**Solutions**:
- Install pre-commit: `pip install pre-commit`
- Install hooks: `pre-commit install`
- Run manually: `pre-commit run --all-files`
- Skip hooks temporarily: `git commit --no-verify`

#### 8. Tests not running
**Problem**: pytest not found or tests failing

**Solutions**:
- Install test dependencies: `pip install -e ".[dev]"`
- Run from project root: `pytest tests/`
- Check Python path: `export PYTHONPATH=.`

### Docker Issues

#### 9. Docker build failures
**Problem**: Container build errors

**Solutions**:
- Check Docker is running: `docker version`
- Build with verbose output: `docker build --no-cache .`
- Check Dockerfile syntax

#### 10. Port already in use
**Problem**: "Port 8000 is already in use"

**Solutions**:
- Use different port: `docker run -p 8080:8000 dependency-doctor`
- Stop conflicting service: `docker ps` and `docker stop <container>`
- Change port in docker-compose.yml

## Getting Help

If you're still having issues:

1. **Check the logs**: Look for detailed error messages
2. **Search issues**: Check [GitHub Issues](https://github.com/onycher/dependency-doctor/issues)
3. **Create an issue**: Include:
   - Operating system and Python version
   - Full error message
   - Steps to reproduce
   - Your configuration (without sensitive data)

## Debugging Tips

### Enable Debug Mode
Add to your `.env`:
```
DEBUG=true
LOG_LEVEL=DEBUG
```

### Verbose Output
Run commands with verbose flags:
```bash
python main.py deps --url <repo> --verbose
pytest tests/ -v
pip install -v -e .
```

### Check System Information
```bash
python main.py version
python --version
pip list
```

### Test Basic Functionality
```bash
# Test without external dependencies
python src/utils/basic_analyzer.py https://github.com/psf/requests

# Test configuration
python -c "from src.utils.config import get_config; print(get_config('DEBUG', 'not_set'))"

# Test logging
python -c "from src.utils.logging import get_logger; get_logger().info('test')"
```

## Performance Tips

1. **Use GitHub token**: Avoids rate limiting
2. **Cache results**: Store analysis results locally
3. **Parallel processing**: Analyze multiple repositories concurrently
4. **Docker**: Use containers for consistent environments

## Security Considerations

1. **Never commit tokens**: Keep `.env` in `.gitignore`
2. **Use read-only tokens**: Minimal required permissions
3. **Regular updates**: Keep dependencies current
4. **Scan dependencies**: Run security scans regularly