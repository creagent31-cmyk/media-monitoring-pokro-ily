import feedparser
import urllib.parse

from config import PROJECTS


def get_news():


    articles=[]


    for project in PROJECTS:

        q = urllib.parse.quote(
            '"' + project + '"'
        )


        url = (
            "https://news.google.com/rss/search?"
            f"q={q}&hl=cs&ceid=CZ:cs"
        )


        feed = feedparser.parse(url)


        for item in feed.entries:


            articles.append({

                "title":
                    item.title,

                "link":
                    item.link,

                "source":
                    item.get(
                        "source",
                        "unknown"
                    ),

                "date":
                    item.get(
                        "published",
                        ""
                    )

            })


    return articles
