def get_keyword_trends(keywords):
    """
    Simulate Exa keyword trend API.
    Replace with real API calls.
    """
    trends = {}
    for kw in keywords:
        trends[kw] = {
            "search_volume": 1000 + len(kw)*10,  # dummy
            "related_queries": [kw + " tips", kw + " strategies", kw + " tools"]
        }
    return trends
