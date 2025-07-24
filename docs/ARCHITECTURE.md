# Architecture Document: Dependency Doctor

## 1. Project Structure

```
dependency-doctor/
  ├── src/
  │   ├── controllers/
  │   │     ├── cli_controller.py      # Click CLI entrypoint
  │   │     ├── api_controller.py      # FastAPI app
  │   │     └── web_controller.py      # rio app
  │   ├── models/
  │   ├── services/
  │   ├── utils/
  │   └── web/                        # rio UI components
  ├── tests/
  ├── docs/
  ├── config/
  ├── main.py                         # Entrypoint (can launch CLI, API, or Web)
  ├── pyproject.toml
  ├── README.md
  └── uv.lock
```

## 2. Interfaces

- **CLI**: Built with Click, provides commands for all core features.
- **API**: Built with FastAPI, exposes endpoints for all core features (for web UI and external integrations).
- **Web UI**: Built with rio, communicates with backend via FastAPI endpoints or direct Python calls.

## 3. Controllers

- `cli_controller.py`: Handles CLI commands using Click.
- `api_controller.py`: Defines FastAPI routes.
- `web_controller.py`: Starts and manages the rio app.

## 4. Core Modules & Responsibilities

- **Services**: Business logic for dependency updates, risk analysis, security scanning, and AI-powered refactoring.
- **Models**: Data structures for dependencies, reports, vulnerabilities, etc.
- **Utils**: Helper functions for file I/O, logging, etc.

## 5. Development Flow

- Core logic lives in `services/` and `models/`.
- Controllers adapt core logic for each interface (CLI, API, Web).
- Tests cover all interfaces and services.

## 6. Extensibility & Modularity

- Each service is modular and replaceable.
- Support for plugins (e.g., for new languages or package managers) in the future.

## 7. Configuration & Environment

- Use `.env` and config files for settings (API keys, database URLs, etc.).
- Support for dry-run and verbose/debug modes.

## 8. Testing

- Unit tests for all modules (pytest).
- Integration tests for end-to-end flows.
- Mock external services (e.g., vulnerability DBs, AI APIs).

## 9. Logging & Error Handling

- Use `structlog` for structured logging.
- Robust error handling with context-rich messages.

## 10. AI Integration

- Abstract AI calls (e.g., to OpenAI, local LLMs) for refactoring.
- Allow for easy swapping of AI backends.

## 11. Security

- Never store sensitive data in code.
- Sanitize all inputs/outputs. 