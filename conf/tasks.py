from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_notification_email(subject, message, from_email, recipient, html_message=None):
    send_mail(
        subject,
        message,
        from_email,
        [recipient],
        fail_silently=True,
        html_message=html_message,
    )
