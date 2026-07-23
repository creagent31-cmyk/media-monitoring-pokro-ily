import smtplib

from email.mime.text import MIMEText

from config import (
    EMAIL_USER,
    EMAIL_PASSWORD,
    EMAIL_TO
)


def send_email(html):

    msg = MIMEText(
        html,
        "html",
        "utf-8"
    )

    msg["Subject"] = (
        "📰 Cresco Media Monitoring"
    )

    msg["From"] = EMAIL_USER

    msg["To"] = ", ".join(
        EMAIL_TO
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
