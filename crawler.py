import urllib.parse
import feedparser
import requests
from bs4 import BeautifulSoup

from config import PROJECTS

# Seznam přímých RSS feedů médií, které chceš hloubkově skenovat
DIRECT_FEEDS = [
    {"source_name": "CzechCrunch", "url": "https://cc.cz/feed/"},
    # Sem můžeš podle potřeby přidat další zdroje, např.:
    # {"source_name": "Lupa", "url": "https://www.lupa.cz/rss/clanky/"},
    # {"source_name": "Hospodářské noviny", "url": "https://hn.cz/rss/"}
]


def _get_full_article_text(url: str) -> str:
    """ Stáhne HTML stránku odkazu a vybere z ní kompletní text obsahu. """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=6)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # Odstraníme balast (skripty, navigaci, patčky)
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()
            return soup.get_text(separator=" ")
    except Exception:
        pass
    return ""


def get_news():
    articles = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # -----------------------------------------------------
    # 1. ZÍSKÁNÍ ZPRÁV Z GOOGLE NEWS (Plošný monitoring internetu)
    # -----------------------------------------------------
    for project in PROJECTS:
        # Hledáme klíčové slovo na celém Google News
        q = urllib.parse.quote(project)
        url = f"https://news.google.com/rss/search?q={q}&hl=cs&ceid=CZ:cs"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)

            for item in feed.entries:
                summary_raw = item.get("summary") or item.get("description", "")
                
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
    # 2. HLUBOČNÍ SKENOVÁNÍ PŘÍMÝCH RSS FEEDŮ
    # -----------------------------------------------------
    for direct_feed in DIRECT_FEEDS:
        try:
            response = requests.get(direct_feed["url"], headers=headers, timeout=10)
            feed = feedparser.parse(response.content)

            for item in feed.entries:
                link = item.get("link", "")
                summary_raw = item.get("summary") or item.get("description", "")
                
                # Prohledáme celý text článku na webové stránce
                full_text = _get_full_article_text(link)
                combined_content = f"{summary_raw} {full_text}"

                articles.append({
                    "title": item.get("title", ""),
                    "link": link,
                    "summary": combined_content,  # Obsahuje celý text článku!
                    "source": direct_feed["source_name"],
                    "date": item.get("published", "")
                })
        except Exception as e:
            print(f"Chyba při stahování feedu {direct_feed['source_name']}: {e}")

    return articles
