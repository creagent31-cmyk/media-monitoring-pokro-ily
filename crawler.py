import urllib.parse
import feedparser
import requests

from config import PROJECTS

# Seznam přímých RSS feedů významných médií (např. CzechCrunch)
DIRECT_FEEDS = [
    {"source_name": "CzechCrunch", "url": "https://cc.cz/feed/"}
]


def get_news():
    articles = []
    
    # Hlavička User-Agent, aby požadavky neblokovaly servery z GitHub Actions
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # -----------------------------------------------------
    # 1. ZÍSKÁNÍ ZPRÁV Z GOOGLE NEWS (hledá i v celém textu)
    # -----------------------------------------------------
    for project in PROJECTS:
        # Hledáme bez natvrdo zadaných uvozovek, aby Google zachytil i skloňování
        q = urllib.parse.quote(project)
        url = f"https://news.google.com/rss/search?q={q}&hl=cs&ceid=CZ:cs"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)

            for item in feed.entries:
                summary_raw = item.get("summary") or item.get("description", "")
                
                # Zjištění názvu zdroje
                source_val = "Google News"
                if hasattr(item, "source"):
                    if isinstance(item.source, dict):
                        source_val = item.source.get("title", "Google News")
                    else:
                        source_val = getattr(item.source, "title", str(item.source))

                articles.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "summary": summary_raw,
                    "source": source_val,
                    "date": item.get("published", "")
                })
        except Exception as e:
            print(f"Chyba při stahování Google News pro {project}: {e}")

    # -----------------------------------------------------
    # 2. ZÍSKÁNÍ ZPRÁV Z PŘÍMÝCH RSS FEEDŮ (např. CzechCrunch)
    # -----------------------------------------------------
    for direct_feed in DIRECT_FEEDS:
        try:
            response = requests.get(direct_feed["url"], headers=headers, timeout=10)
            feed = feedparser.parse(response.content)

            for item in feed.entries:
                summary_raw = item.get("summary") or item.get("description", "")

                articles.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "summary": summary_raw,
                    "source": direct_feed["source_name"],
                    "date": item.get("published", "")
                })
        except Exception as e:
            print(f"Chyba při stahování feedu {direct_feed['source_name']}: {e}")

    return articles
