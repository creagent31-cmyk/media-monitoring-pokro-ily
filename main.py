from crawler import get_news
from filter import process_articles

from database import (
    init,
    exists,
    save
)

from report import create
from email_sender import send_email



def main():

    print("🚀 Spouštím Cresco Media Monitor")


    # vytvoření databáze
    init()


    print("🔎 Stahuji články...")


    articles = get_news()


    print(
        f"Nalezeno článků: {len(articles)}"
    )


    print("🧠 Filtruji relevantní články...")


    filtered = process_articles(
        articles
    )


    print(
        f"Relevantních článků: {len(filtered)}"
    )


    new_articles = []


    for article in filtered:


        if exists(
            article["link"]
        ):

            continue


        save(
            article
        )


        new_articles.append(
            article
        )



    if not new_articles:

        print(
            "Žádné nové články"
        )

        return



    print(
        "📧 Vytvářím report..."
    )


    html = create(
        new_articles
    )


    send_email(
        html
    )


    print(
        "✅ Hotovo"
    )



if __name__ == "__main__":

    main()
