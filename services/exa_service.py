import requests

def get_trending_keywords(topic):
    exa_api = "https://api.exa.ai/v1/keywords"
    headers = {
        "Authorization": "Bearer {EXA_API_KEY}"
    }
    params = {
        "query": topic,
        "num_keywords": 10
    }
    
    response = requests.get(exa_api, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Assuming the keywords are inside data['keywords'], adjust as needed
        keywords = data.get("keywords", [])
        return keywords
    else:
        # Handle error or return empty list
        print(f"Error: Exa API request failed with status code {response.status_code}")
        return []
