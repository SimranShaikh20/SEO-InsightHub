import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.ai/v1/chat/completions"

def generate_seo_tips(summary_text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = (
        f"You are an SEO expert. Given this website SEO summary, "
        f"provide top 5 quick SEO improvement steps with explanations:\n\n{summary_text}"
    )

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You provide concise SEO tips."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 300,
        "temperature": 0.7,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating SEO tips: {e}"
