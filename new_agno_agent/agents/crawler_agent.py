from agno_agent import Agent
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class CrawlerAgent(Agent):
    def __init__(self):
        super().__init__("CrawlerAgent")
    
    def crawl_website(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract SEO data
            data = {
                'url': url,
                'domain': urlparse(url).netloc,
                'title': self._get_title(soup),
                'meta_description': self._get_meta_description(soup),
                'headings': self._get_headings(soup),
                'images': self._get_images(soup),
                'links': self._get_links(soup, url),
                'status_code': response.status_code,
                'load_time': response.elapsed.total_seconds()
            }
            return data
        except Exception as e:
            self.log_error(f"Error crawling {url}: {str(e)}")
            return None
    
    def _get_title(self, soup):
        title = soup.find('title')
        return title.text if title else None
    
    def _get_meta_description(self, soup):
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta['content'] if meta and 'content' in meta.attrs else None
    
    def _get_headings(self, soup):
        headings = {}
        for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            elements = soup.find_all(level)
            headings[level] = [el.text.strip() for el in elements]
        return headings
    
    def _get_images(self, soup):
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        return images
    
    def _get_links(self, soup, base_url):
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if not href.startswith('http'):
                href = base_url + href
            links.append({
                'href': href,
                'text': a.text.strip(),
                'title': a.get('title', '')
            })
        return links