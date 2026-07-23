import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    EMAIL_USER,
    EMAIL_PASSWORD,
    EMAIL_TO
)


def send_email(html_content):
    """
    Odešle HTML report přes Gmail SMTP
    """

    if not EMAIL_USER or not EMAIL_PASSWORD:
        raise Exception(
            "Chybí EMAIL_USER nebo EMAIL_PASSWORD"
        )


    msg = MIMEMultipart("alternative")

    msg["Subject"] = (
        "📰 Cresco Media Monitoring"
    )

    msg["From"] = (
        f"Cresco Media Monitor <{EMAIL_USER}>"
    )

    msg["To"] = ", ".join(
        EMAIL_TO
    )


    # HTML tělo emailu
    html_part = MIMEText(
        html_content,
        "html",
        "utf-8"
    )

    msg.attach(
        html_part
    )


    try:

        print(
            "📨 Připojuji se k Gmail SMTP..."
        )


        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:


            server.login(
                EMAIL_USER,
                EMAIL_PASSWORD
            )


            server.sendmail(
                EMAIL_USER,
                EMAIL_TO,
                msg.as_string()
            )


        print(
            "✅ Email úspěšně odeslán"
        )


    except Exception as e:

        print(
            f"❌ Chyba při odesílání emailu: {e}"
        )

        raise
