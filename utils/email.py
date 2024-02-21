from typing import List
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection


def send_mail(self, to: List[str], subject, email_plaintext_message=None, email_html_message=None):
    # render email text
    with get_connection(host=settings.EMAIL_HOST,
                        port=settings.EMAIL_PORT,
                        username=settings.EMAIL_HOST_USER,
                        password=settings.EMAIL_HOST_PASSWORD,
                        use_tls=settings.EMAIL_USE_TLS) as connection:
        msg = EmailMultiAlternatives(
            # title:
            subject=subject,
            # message:
            body=email_plaintext_message,
            # from:
            from_email=settings.EMAIL_HOST_USER,
            # to:
            to=to,
            connection=connection
        )
        if email_html_message:
            msg.attach_alternative(email_html_message, "text/html")
        msg.send()
