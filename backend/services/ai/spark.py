import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment from .env.development at project root
# backend/services/ai/spark.py -> parents[3] = repo root
_ROOT_ENV = Path(__file__).resolve().parents[3] / ".env.development"
load_dotenv(dotenv_path=_ROOT_ENV, override=False)
# Fallback: also support .env.development in backend/ and cwd for local dev flexibility
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env.development", override=False)
load_dotenv(override=False)

# Meta Spark 1.1 configuration — per API reference https://api.meta.ai/v1
# Primary env var is MODEL_API_KEY (Bearer token), keep SPARK_* for backwards compat
# Snippet reference:
#   from openai import OpenAI
#   client = OpenAI(base_url="https://api.meta.ai/v1", api_key=os.environ.get("MODEL_API_KEY"))
#   client.chat.completions.create(model="muse-spark-1.1", messages=[...])
MODEL_API_KEY = (
    os.getenv("MODEL_API_KEY")
    or os.getenv("SPARK_API_KEY")
    or os.getenv("META_SPARK_API_KEY")
    or os.getenv("LLM_API_KEY")
    or os.getenv("GEMINI_KEY")  # backwards compat, deprecated
)
# Base URL per docs: https://api.meta.ai/v1 (Auth: Authorization: Bearer $MODEL_API_KEY)
SPARK_API_KEY = MODEL_API_KEY  # alias for backwards compat
SPARK_API_URL = (
    os.getenv("SPARK_API_URL")
    or os.getenv("META_SPARK_API_URL")
    or os.getenv("MODEL_API_URL")
    or "https://api.meta.ai/v1"
)
# Model per snippet: muse-spark-1.1
SPARK_MODEL = os.getenv("SPARK_MODEL") or os.getenv("MODEL_NAME") or "muse-spark-1.1"


def _get_openai_client():
    """Lazy OpenAI client creation matching snippet exactly."""
    if not MODEL_API_KEY:
        return None
    try:
        from openai import OpenAI
    except ImportError:
        return None
    return OpenAI(
        base_url=SPARK_API_URL,
        api_key=MODEL_API_KEY,
    )


def _get_async_openai_client():
    """Async variant for use in async contexts."""
    if not MODEL_API_KEY:
        return None
    try:
        from openai import AsyncOpenAI
    except ImportError:
        return None
    return AsyncOpenAI(
        base_url=SPARK_API_URL,
        api_key=MODEL_API_KEY,
    )


class AIService:
    def __init__(self):
        self.api_key = MODEL_API_KEY
        self.api_url = SPARK_API_URL.rstrip("/")
        self.model = SPARK_MODEL
        self.timeout = 30.0

    async def classify_ticket(self, message: str):
        if not self.api_key:
            return {"category": "General Support", "priority": "low"}

        prompt = f"""
        Analyze the following customer support message and return a JSON object with:
        - "category": (e.g., Technical Support, Billing, Feature Request, General Inquiry)
        - "priority": ("low" or "high") based on the urgency and sentiment of the message.

        Message: "{message}"

        Return ONLY the JSON object.
        """

        try:
            # Use OpenAI SDK as per snippet: client.chat.completions.create(model="muse-spark-1.1", ...)
            client = _get_async_openai_client()
            if client is not None:
                # Async path (preferred for FastAPI)
                response = await client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.choices[0].message.content
                client_to_close = client
            else:
                # Fallback to sync client in thread if AsyncOpenAI not available
                import asyncio

                def _sync_call():
                    sync_client = _get_openai_client()
                    if sync_client is None:
                        raise RuntimeError("OpenAI SDK not installed")
                    resp = sync_client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    return resp.choices[0].message.content

                content = await asyncio.to_thread(_sync_call)
                client_to_close = None

            if not content:
                raise ValueError("Empty response from Meta Spark")

            # Content may be JSON string or already parsed
            if isinstance(content, dict):
                result = content
            else:
                result = json.loads(content.strip())

            # Ensure expected keys
            if "category" not in result or "priority" not in result:
                # Try to handle markdown code fences
                text = content.strip().strip("`")
                if text.startswith("json"):
                    text = text[4:].strip()
                result = json.loads(text)

            return result
        except Exception as e:
            print(f"Error classifying ticket with Meta Spark ({self.model}): {e}")
            # Try to close async client if needed
            try:
                if "client_to_close" in locals() and client_to_close is not None:
                    await client_to_close.close()
            except Exception:
                pass
            return {
                "category": "General Support",
                "priority": "low",
            }

    async def draft_answer(self, customer_name: str, message: str):
        if not self.api_key:
            return "Unable to generate a draft. AI service not available."

        prompt = f"""
        You are a helpful customer support agent. 
        Write a concise, professional, and empathetic response to the following customer message.
        
        Customer Name: {customer_name}
        Customer Message: "{message}"
        
        Return ONLY the response text.
        """

        try:
            client = _get_async_openai_client()
            if client is not None:
                response = await client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.choices[0].message.content
                client_to_close = client
            else:
                import asyncio

                def _sync_call():
                    sync_client = _get_openai_client()
                    if sync_client is None:
                        raise RuntimeError("OpenAI SDK not installed")
                    resp = sync_client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    return resp.choices[0].message.content

                content = await asyncio.to_thread(_sync_call)
                client_to_close = None

            if not content:
                raise ValueError("Empty response from Meta Spark")

            try:
                if "client_to_close" in locals() and client_to_close is not None:
                    await client_to_close.close()
            except Exception:
                pass

            if isinstance(content, dict):
                return content.get("draft") or content.get("content") or str(content)
            return str(content).strip()
        except Exception as e:
            print(f"Error drafting answer with Meta Spark ({self.model}): {e}")
            try:
                if "client_to_close" in locals() and client_to_close is not None:
                    await client_to_close.close()
            except Exception:
                pass
            return "Sorry, I encountered an error while drafting the response. Please try again."


ai_service = AIService()

# Sync helper matching snippet exactly for scripts/notebooks
def get_sync_client():
    """Return OpenAI client exactly as in snippet."""
    from openai import OpenAI

    return OpenAI(
        base_url=SPARK_API_URL,
        api_key=MODEL_API_KEY,
    )
