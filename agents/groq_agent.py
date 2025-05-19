import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.ai/v1/completions'  # Example URL, confirm actual endpoint

def get_seo_recommendations(seo_summary):
    prompt = f"""
    You are an SEO expert. Based on the following website SEO summary, give 5 quick improvement tips:
    {seo_summary}
    """
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json',
    }
    json_data = {
        "model": "mixtral-8x7b-32768",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=json_data)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error fetching SEO tips: {e}"
