import urllib.parse
import feedparser
import requests

from config import PROJECTS


def get_news():
    articles = []
    
    # Hlavička, aby nás Google News neblokoval na GitHub Actions
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for project in PROJECTS:
        # Hledáme název projektu BEZ uvozovek – zachytí i skloňování a volnější shody
        q = urllib.parse.quote(project)

        url = (
            "https://news.google.com/rss/search?"
            f"q={q}&hl=cs&ceid=CZ:cs"
        )

        try:
            # Stáhneme feed přes requests s User-Agentem
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)

            for item in feed.entries:
                # Vytáhnutí náhledu/perexu článku (summary/description)
                summary_raw = item.get("summary") or item.get("description", "")
                
                # Zdroje v Google News mají název buď jako objekt, nebo řetězec v item.source.title
                source_val = "unknown"
                if hasattr(item, "source"):
                    source_val = item.source.get("title", "unknown") if isinstance(item.source, dict) else getattr(item.source, "title", str(item.source))

                articles.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "summary": summary_raw,
                    "source": source_val,
                    "date": item.get("published", "")
                })
        except Exception as e:
            print(f"Chyba při stahování feedu pro {project}: {e}")

    return articles
