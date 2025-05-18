import requests

def update_wordpress_post(post_id, title=None, content=None, meta_desc=None, token=None, site_url=None):
    url = f"{site_url}/wp-json/wp/v2/posts/{post_id}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {}
    if title:
        data['title'] = title
    if content:
        data['content'] = content
    if meta_desc:
        data['meta'] = {'description': meta_desc}
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()
