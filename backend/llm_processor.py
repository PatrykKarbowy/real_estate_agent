import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def parse_query(user_query: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "google/gemini-2.5-pro-exp-03-25:free",
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": user_query}]}
        ],
    }

    response = requests.post(OPENROUTER_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", {})
    else:
        return {"error": f"API request failed with status {response.status_code}"}
