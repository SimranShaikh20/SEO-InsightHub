import requests
from bs4 import BeautifulSoup

def crawl_website(url):
    """Fetch page HTML and extract SEO info"""
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.title.string if soup.title else ''
        meta_desc = ''
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get('content', '')

        headings = {}
        for i in range(1, 4):  # H1, H2, H3
            tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [tag.get_text(strip=True) for tag in tags]

        return {
            'url': url,
            'title': title,
            'meta_description': meta_desc,
            'headings': headings
        }
    except Exception as e:
        return {'url': url, 'error': str(e)}
