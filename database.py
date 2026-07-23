import sqlite3

DB = "media.db"


def init():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS articles(
        link TEXT PRIMARY KEY,
        title TEXT,
        summary TEXT,
        sentiment TEXT,
        relevance INTEGER
    )
    """)

    conn.commit()
    conn.close()


def exists(link):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "SELECT link FROM articles WHERE link=?",
        (link,)
    )

    result = c.fetchone()
    conn.close()

    return result is not None


def save(article):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    raw_summary = article.get("summary") or article.get("description", "")
    if isinstance(raw_summary, dict):
        summary = str(raw_summary.get("value", ""))
    else:
        summary = str(raw_summary)

    c.execute("""
    INSERT OR IGNORE INTO articles
    VALUES(?,?,?,?,?)
    """,
    (
        str(article.get("link", "")),
        str(article.get("title", "")),
        summary,
        str(article.get("sentiment", "🟡 Neutrální")),
        article.get("importance") or article.get("relevance", 1)
    ))

    conn.commit()
    conn.close()
