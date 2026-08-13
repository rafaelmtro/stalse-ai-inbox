# Use a slim Python image
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (openai + httpx for Muse Spark 1.1 via https://api.meta.ai/v1)
RUN uv sync --frozen --no-cache

# Copy the rest of the application (respects .dockerignore: ignores .venv, __pycache__, *.db)
COPY . .

# Ensure correct venv after COPY (host .venv ignored, but ensure deps are synced)
RUN uv sync --frozen --no-cache

# Create database directory if it doesn't exist
RUN mkdir -p database

# Environment variables are injected via docker-compose env_file: .env.development (project root)
# Do not copy .env.development into image; runtime injection is used instead

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
