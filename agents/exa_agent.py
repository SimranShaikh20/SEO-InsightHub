def get_keyword_trends(keywords):
    """Simulated trending keywords data (replace with Exa API in future)"""
    trending = {}
    for kw in keywords:
        trending[kw] = {
            'search_volume': 1000,  # Dummy static number
            'related_queries': [kw + ' tips', kw + ' best practices', 'how to ' + kw]
        }
    return trending
