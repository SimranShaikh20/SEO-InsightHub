import requests

def crawl_website(url):
    """
    Simulate Firecrawl crawling: returns dummy SEO data for given URL.
    Replace with real Firecrawl API calls if available.
    """
    # Dummy example response
    return {
        "url": url,
        "title": f"Title of {url}",
        "meta_description": f"Meta description of {url}",
        "headings": {
            "h1": ["Heading 1 for " + url],
            "h2": ["Subheading 1", "Subheading 2"]
        },
        "page_speed": 75,  # example score
        "image_alt_text_count": 10,
        "keyword_density": {"seo": 2.5, "marketing": 1.8}
    }
