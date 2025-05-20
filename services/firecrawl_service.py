import requests

def crawl_site(url):
    firecrawl_api = "https://api.firecrawl.dev/v1/crawl"
    headers = {
        "Authorization": "Bearer {FIRECRAWL_API_KEY}"
    }
    data = {
        "url": url,
        "includeText": True,
        "includeHtml": False,
        "includeScreenshots": False
    }
    response = requests.post(firecrawl_api, json=data, headers=headers)
    result = response.json()

    # Example: Extract useful SEO info from the response
    # Adjust these keys based on Firecrawl API response structure
    page_title = result.get("title", "No Title Found")

    # Suppose headings are in result["headings"] as a list of strings
    headings = result.get("headings", [])

    # Suppose meta tags are in result["meta"] as dict {name: content}
    meta = result.get("meta", {})

    # Return structured data
    return {
        "title": page_title,
        "headings": headings,
        "meta": meta
    }
