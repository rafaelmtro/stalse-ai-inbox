# LLM Email Sorter - Backend

This is the FastAPI backend for the LLM Email Sorter system, responsible for managing support tickets and integrating with the Meta Spark 1.1 AI service.

## Backend Stack

- **FastAPI**: Modern, high-performance web framework for building APIs.
- **Python (3.10+)**: Leveraging modern asynchronous features.
- **uv**: Fast Python package manager and virtual environment tool.
- **SQLite & SQLAlchemy**: Efficient and lightweight persistence layer.
- **Meta Spark 1.1 API (`muse-spark-1.1` via `openai` SDK `base_url="https://api.meta.ai/v1"`)**: AI-powered classification and drafting.
- **pytest**: Robust testing framework for units and API integration.

## Project Structure

```text
backend/
├── database/            # SQLAlchemy models and SQLite setup
├── services/
│   └── ai/              # Meta Spark 1.1 integration layer (spark.py)
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
3.  **Environment Variables**: Create a `.env.development` file in the project root with your Meta Spark 1.1 API Key (`MODEL_API_KEY` for `https://api.meta.ai/v1`):
    ```
    MODEL_API_KEY=your_api_key_here
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
