import requests

def get_seo_advice(summary):
    groq_api = "https://api.groq.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_GROQ_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are an SEO expert."},
            {"role": "user", "content": summary}
        ]
    }
    response = requests.post(groq_api, json=payload, headers=headers)
    return response.json()['choices'][0]['message']['content']
