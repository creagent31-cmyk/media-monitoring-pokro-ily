import sqlite3


DB="media.db"



def init():

    conn=sqlite3.connect(DB)

    c=conn.cursor()


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

    conn=sqlite3.connect(DB)

    c=conn.cursor()


    c.execute(
        "SELECT link FROM articles WHERE link=?",
        (link,)
    )


    result=c.fetchone()

    conn.close()


    return result is not None



def save(article):

    conn=sqlite3.connect(DB)

    c=conn.cursor()


    c.execute("""
    INSERT OR IGNORE INTO articles
    VALUES(?,?,?,?,?)
    """,
    (

        article["link"],
        article["title"],
        article["summary"],
        article["sentiment"],
        article["relevance"]

    ))


    conn.commit()
    conn.close()
