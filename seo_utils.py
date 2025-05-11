import requests
import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_KEY = os.getenv("FIRECRAWL_API_KEY")
EXA_KEY = os.getenv("EXA_API_KEY")

def crawl_website(url):
    endpoint = "https://api.firecrawl.dev/v1/crawl"
    headers = {"Authorization": f"Bearer {FIRECRAWL_KEY}"}
    data = {"url": url, "includeMetadata": True}

    try:
        response = requests.post(endpoint, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_trending_keywords(query):
    endpoint = "https://api.exa.ai/search"
    headers = {
        "Authorization": f"Bearer {EXA_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"query": query}

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        results = response.json().get("results", [])
        return [res.get("title", "") for res in results[:3]]
    except Exception as e:
        return [f"Error fetching keywords: {str(e)}"]
