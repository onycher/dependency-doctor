# TODO: Dependency Doctor Implementation Plan

## 1. Project Foundation

### 1.1 Configuration
- [x] Create `.env` file and add to `.gitignore`
- [x] Implement config loader utility in `src/utils/config.py`
- [x] Add sample config values (API keys, debug flags)
- [x] Add `GITHUB_TOKEN` for authenticated requests

### 1.2 Logging
- [x] Set up `structlog` in `src/utils/logging.py`
- [x] Add a basic log statement to each interface entrypoint

---

## 2. Core Interfaces (Skeletons)

### 2.1 CLI (Click)
- [x] Implement `doctor status` command
- [x] Implement `doctor deps` command (from GitHub, pyproject.toml and requirements.txt)
- [x] Implement `doctor check-updates` command
- [ ] Add support for listing transitive dependencies
- [ ] Implement `doctor update` command (trigger update)
- [ ] Implement `doctor security-scan` command

### 2.2 API (FastAPI)
- [x] Implement `/status` endpoint
- [ ] Implement `/dependencies` endpoint (list)
- [ ] Implement `/update` endpoint (trigger update)
- [ ] Implement `/security` endpoint (scan for vulnerabilities)

### 2.3 Web UI (rio)
- [x] Create rio app entrypoint
- [x] Implement dashboard page (calls `/status`)
- [ ] Implement dependencies page (calls `/dependencies`)
- [ ] Implement update trigger UI
- [ ] Implement security scan UI

---

## 3. Core Services

### 3.1 DependencyService
- [x] Implement function to parse and list dependencies (from GitHub)
- [x] Implement function to check for outdated dependencies (with intelligent comparison)

### 3.2 SecurityService
- [x] Implement function to scan dependencies for vulnerabilities
- [ ] Integrate with public vulnerability database (stub/mock first)

### 3.3 RiskAnalysisService
- [ ] Implement function to analyze update impact (stub first)

### 3.4 RefactorService
- [ ] Implement AI refactor stub (returns mock suggestions)

---

## 4. Integration

- [ ] Wire CLI commands to services
- [ ] Wire API endpoints to services
- [ ] Wire Web UI to API endpoints

---

## 5. Testing

### 5.1 Unit Tests
- [x] Add tests for config loader
- [x] Add tests for logging setup
- [x] Add tests for all log levels, structured data, logger naming, and exception logging
- [x] Add tests for GitHub scanner service (pyproject.toml and requirements.txt)
- [x] Add tests for update checker service (with version comparison logic)
- [x] Add tests for security scanner service
- [ ] Add tests for each remaining service

### 5.2 Integration Tests
- [ ] Test CLI commands end-to-end
- [ ] Test API endpoints end-to-end
- [ ] Test Web UI flows (manual or automated)

---

## 6. Advanced Features

- [ ] Implement automated dependency update logic
- [ ] Implement risk and impact reporting
- [ ] Implement security alerting and suggestions
- [ ] Integrate real AI-powered code refactoring

---

## 7. Polish & Documentation

- [ ] Improve error handling and user feedback
- [ ] Add docstrings and comments
- [ ] Update documentation (README, usage guides)
- [ ] Add Chinese README version

---

## 8. CI/CD

- [ ] Set up GitHub Actions for linting, testing, and deployment 