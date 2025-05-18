import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.title.string if soup.title else ''
    meta_desc = ''
    for tag in soup.find_all('meta'):
        if tag.get('name', '').lower() == 'description':
            meta_desc = tag.get('content', '')
            break
    
    text = soup.get_text(separator=' ', strip=True)
    
    headings = {f'h{i}': [h.get_text(strip=True) for h in soup.find_all(f'h{i}')] for i in range(1,7)}
    
    images = [(img.get('alt', ''), img.get('src')) for img in soup.find_all('img')]
    
    return {
        'title': title,
        'meta_desc': meta_desc,
        'text': text,
        'headings': headings,
        'images': images
    }
