import logging
import urllib.parse

import feedparser
import requests
import trafilatura
from bs4 import BeautifulSoup

from config import PROJECTS


# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ==========================================================
# HTTP SESSION
# ==========================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    )
}

session = requests.Session()
session.headers.update(HEADERS)


# ==========================================================
# RSS FEEDY
# ==========================================================

DIRECT_FEEDS = [

    {
        "source_name": "CzechCrunch",
        "url": "https://cc.cz/feed/"
    },

    # sem můžeš jednoduše přidávat další

]


# ==========================================================
# STAŽENÍ CELÉHO ČLÁNKU
# ==========================================================

def _get_full_article_text(url: str) -> str:

    try:

        downloaded = trafilatura.fetch_url(url)

        if downloaded:

            text = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=False
            )

            if text and len(text) > 300:
                return text

    except Exception:
        pass

    # fallback přes BeautifulSoup

    try:

        response = session.get(url, timeout=5)

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup(
            [
                "script",
                "style",
                "header",
                "footer",
                "nav",
                "aside",
                "form"
            ]
        ):
            tag.decompose()

        text = soup.get_text(" ")

        if len(text) < 300:
            return ""

        return text

    except Exception:

        return ""


# ==========================================================
# GOOGLE NEWS
# ==========================================================

def _google_news():

    articles = []

    for project in PROJECTS:

        query = urllib.parse.quote(
            f'"{project}" when:14d'
        )

        url = (
            "https://news.google.com/rss/search?"
            f"q={query}"
            "&hl=cs"
            "&ceid=CZ:cs"
        )

        try:

            response = session.get(
                url,
                timeout=8
            )

            feed = feedparser.parse(
                response.content
            )

            for item in feed.entries:

                source = "Google News"

                if hasattr(item, "source"):

                    if isinstance(item.source, dict):

                        source = item.source.get(
                            "title",
                            "Google News"
                        )

                articles.append({

                    "title":
                        item.get("title", ""),

                    "link":
                        item.get("link", ""),

                    "summary":
                        item.get(
                            "summary",
                            ""
                        ),

                    "source":
                        source,

                    "date":
                        item.get(
                            "published",
                            ""
                        )

                })

        except Exception as e:

            logging.warning(
                f"Google News chyba ({project}): {e}"
            )

    return articles


# ==========================================================
# RSS FEEDY
# ==========================================================

def _rss_feeds():

    articles = []

    for feed_info in DIRECT_FEEDS:

        try:

            response = session.get(
                feed_info["url"],
                timeout=8
            )

            feed = feedparser.parse(
                response.content
            )

            for item in feed.entries:

                title = item.get(
                    "title",
                    ""
                )

                summary = item.get(
                    "summary",
                    ""
                )

                link = item.get(
                    "link",
                    ""
                )

                full_text = _get_full_article_text(
                    link
                )

                content = (
                    summary
                    + "\n\n"
                    + full_text
                )

                articles.append({

                    "title":
                        title,

                    "link":
                        link,

                    "summary":
                        content,

                    "source":
                        feed_info["source_name"],

                    "date":
                        item.get(
                            "published",
                            ""
                        )

                })

        except Exception as e:

            logging.warning(
                f"RSS chyba ({feed_info['source_name']}): {e}"
            )

    return articles


# ==========================================================
# DEDUPLIKACE
# ==========================================================

def _deduplicate(articles):

    unique = {}

    for article in articles:

        key = article["link"].strip().lower()

        if key:

            unique[key] = article

    return list(
        unique.values()
    )


# ==========================================================
# MAIN
# ==========================================================

def get_news():

    logging.info(
        "Načítám Google News..."
    )

    google_articles = _google_news()

    logging.info(
        "Načítám RSS..."
    )

    rss_articles = _rss_feeds()

    articles = (
        google_articles
        + rss_articles
    )

    articles = _deduplicate(
        articles
    )

    logging.info(
        f"Nalezeno {len(articles)} unikátních článků."
    )

    return articles
