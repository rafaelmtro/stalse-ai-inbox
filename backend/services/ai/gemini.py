import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GEMINI_KEY = os.getenv("GEMINI_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def classify_ticket(self, message: str):
        prompt = f"""
        Analyze the following customer support message and return a JSON object with:
        - "category": (e.g., Technical Support, Billing, Feature Request, General Inquiry)
        - "priority": ("low" or "high") based on the urgency and sentiment of the message.

        Message: "{message}"

        Return ONLY the JSON object.
        """
        
        try:
            # Use synchronous call for now as the library's async support varies by version
            # In a real high-scale app, we'd use a thread pool or a truly async client
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response text (cleaning any markdown blocks if present)
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            return json.loads(content)
        except Exception as e:
            print(f"Error classifying ticket with Gemini: {e}")
            # Fallback values
            return {
                "category": "General Support",
                "priority": "low"
            }

ai_service = AIService()
