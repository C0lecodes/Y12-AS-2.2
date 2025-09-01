import requests, re

BASE_URL = "https://hdtodayz.to"
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def get(title: str) -> str:
    search_url = f"{BASE_URL}/search/{title.replace(' ', '-')}"
    try:
        response = session.get(search_url, timeout=3)
        html = response.text
    except requests.exceptions.RequestException:
        # Covers timeouts, no connection, DNS failure, etc.
        return "No internet connection"

    match = re.search(r'/movie/watch-[^/"]*?-(\d+)', html)
    if match:
        return f"{BASE_URL}/movie/watch-{match.group(1)}"
    return "No movie"
