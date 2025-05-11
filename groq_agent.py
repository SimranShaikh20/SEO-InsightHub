import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_seo_tips(issues, keywords):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
A website has the following SEO issues:

{issues}

Trending keywords: {keywords}

Please give:

1. Top 5 quick SEO improvement steps
2. A short motivational summary
"""

    payload = {
        "messages": [
            {"role": "system", "content": "You are an SEO expert assistant."},
            {"role": "user", "content": prompt}
        ],
        "model": "mixtral-8x7b-32768"
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
