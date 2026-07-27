import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROK_API_KEY")

if not api_key or api_key == "xai-paste-your-grok-key-here":
    print("API key is missing or still set to the placeholder.")
else:
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get("https://api.x.ai/v1/models", headers=headers)
    if response.status_code == 200:
        models = response.json().get("data", [])
        print("AVAILABLE GROK MODELS:")
        for m in models:
            print("-", m.get("id"))
    else:
        print("Failed to fetch models:", response.status_code, response.text)
