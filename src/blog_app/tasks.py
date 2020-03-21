from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def email_task(title, blog_name, post_id, email):
    send_mail(
        f'New post in {blog_name}',
        None,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=f'<a href="http://localhost:8000/posts/{post_id}/">{title}</a>'
    )
