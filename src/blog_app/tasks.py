from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from time import sleep


@shared_task
def email_task(title, blog_name, post_id, email):
    send_mail(
        f'New post in {title}', 
        None,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=f'<a href="http://localhost:8000/post/{post_id}/">{title}</a>'
    )
