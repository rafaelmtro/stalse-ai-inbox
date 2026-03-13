import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GEMINI_KEY = os.getenv("GEMINI_KEY")

class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None

    async def classify_ticket(self, message: str):
        if not self.client:
            return {"category": "General Support", "priority": "low"}

        prompt = f"""
        Analyze the following customer support message and return a JSON object with:
        - "category": (e.g., Technical Support, Billing, Feature Request, General Inquiry)
        - "priority": ("low" or "high") based on the urgency and sentiment of the message.

        Message: "{message}"

        Return ONLY the JSON object.
        """
        
        try:
            # Use generate_content with JSON mode if supported or just standard response
            response = self.client.models.generate_content(
                model='gemini-3.1-flash-lite-preview',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                ),
            )
            
            # The new SDK might return the object directly depending on how it's called
            # but usually it's in response.text
            return json.loads(response.text)
        except Exception as e:
            print(f"Error classifying ticket with Gemini: {e}")
            # Fallback values
            return {
                "category": "General Support",
                "priority": "low"
            }

ai_service = AIService()
