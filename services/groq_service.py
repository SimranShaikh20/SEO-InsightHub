import requests
from config import GROQ_API_KEY

def get_seo_advice(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mixtral-8x7b-32768",  # or your specified model
        "messages": [
            {"role": "system", "content": "You're an SEO expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, json=data, headers=headers)
    result = response.json()

    # Check if 'choices' exist in response
    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        # Print/log error and return fallback message
        print("GROQ API error:", result)
        return "⚠️ Error: Unable to fetch SEO advice from GROQ AI."
