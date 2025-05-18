import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def rewrite_text(text, keywords):
    prompt = (
        f"Improve the following meta description for SEO using these keywords: {', '.join(keywords)}.\n\n"
        f"Original: {text}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
