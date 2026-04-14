# Stalse AI Inbox - Backend

This is the FastAPI backend for the Stalse AI Inbox system, responsible for managing support tickets and integrating with the Gemini AI service.

## Backend Stack

- **FastAPI**: Modern, high-performance web framework for building APIs.
- **Python (3.10+)**: Leveraging modern asynchronous features.
- **uv**: Fast Python package manager and virtual environment tool.
- **SQLite & SQLAlchemy**: Efficient and lightweight persistence layer.
- **Gemini API**: AI-powered classification and drafting.
- **pytest**: Robust testing framework for units and API integration.

## Project Structure

```text
backend/
├── database/            # SQLAlchemy models and SQLite setup
├── services/
│   └── ai/              # Gemini integration layer
├── tests/               # API and unit test suite
├── main.py              # Application entry point (FastAPI)
├── pyproject.toml       # Dependencies and project metadata (uv)
└── seed.py              # Database initialization and seeding
```

## Setup and Running

To run the backend independently, follow these steps:

1.  **Install `uv`**: If not already installed, visit [uv's documentation](https://github.com/astral-sh/uv).
2.  **Install dependencies**:
    ```bash
    uv sync
    ```
3.  **Environment Variables**: Create a `.env` file with your Gemini API Key:
    ```
    GEMINI_KEY=your_api_key_here
    ```
4.  **Seed the database**:
    ```bash
    uv run python seed.py
    ```
5.  **Run the application**:
    ```bash
    uv run uvicorn main:app --reload
    ```

## Testing

To run the test suite, use the following command:

```bash
uv run pytest
```
