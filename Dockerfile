# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .
COPY src/ src/
COPY examples/ examples/
COPY main.py .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Default command
CMD ["python", "main.py", "--help"]

# Expose ports for web and API interfaces
EXPOSE 8000 8001

# Add labels
LABEL maintainer="onycher <928520+onycher@users.noreply.github.com>"
LABEL description="Dependency Doctor - Python dependency analysis tool"
LABEL version="0.1.0"