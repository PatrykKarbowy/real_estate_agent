import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

conversation_history = []


def parse_query(user_query: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    conversation_history.append({
        "role": "user",
        "content": [{"type": "text", "text": user_query}]
    })

    payload = {
        "model": "google/gemini-2.5-pro-exp-03-25:free",
        "messages": conversation_history
    }

    response = requests.post(OPENROUTER_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        assistant_response = data.get("choices", [{}])[0].get("message", {}).get("content", {})

        conversation_history.append({
            "role": "assistant",
            "content": [{"type": "text", "text": assistant_response}]
        })

        return assistant_response
    else:
        return {"error": f"API request failed with status {response.status_code}. {response.text}"}
