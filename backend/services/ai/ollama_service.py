import os
import json
import ollama
from ollama import Client

class AIService:
    def __init__(self):
        # Default Ollama host is http://localhost:11434, but inside Docker it should be http://ollama:11434
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = Client(host=host)
        self.model = "gemma3:270m"

    async def classify_ticket(self, message: str):
        prompt = f"""
        Analyze the following customer support message and return a JSON object with:
        - "category": (e.g., Technical Support, Billing, Feature Request, General Inquiry)
        - "priority": ("low" or "high") based on the urgency and sentiment of the message.

        Message: "{message}"

        Return ONLY the JSON object.
        """
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            # The ollama-python client returns a response object with a 'message' field
            content = response.message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"Error classifying ticket with Ollama ({self.model}): {e}")
            # Fallback values
            return {
                "category": "General Support",
                "priority": "low"
            }

ai_service = AIService()
