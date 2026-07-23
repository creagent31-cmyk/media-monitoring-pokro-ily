from crawler import get_news

from database import (
    init,
    exists,
    save
)

from ai import analyze

from report import create

from email_sender import send



def main():


    init()


    new=[]


    for article in get_news():


        if exists(
            article["link"]
        ):
            continue


        result=analyze(
            article["title"]
        )


        article["summary"]=result


        article["sentiment"]="AI"

        article["relevance"]=5


        save(article)


        new.append(article)



    if new:

        html=create(
            new
        )

        send(html)



if __name__=="__main__":

    main()
