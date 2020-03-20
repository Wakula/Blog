from django.db import models
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string


class Blog(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField()
    author = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(get_user_model(), blank=True, related_name='subscribed_blogs')

    def user_is_subscribed(self, user):
        return user in self.subscribers.all()

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    users_that_have_read = models.ManyToManyField(get_user_model(), blank=True, related_name='read_posts')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in self.blog.subscribers.all():
            user.email_user(
                f'New post in {self.blog}', None,
                html_message=f'<a href="http://localhost:8000/post/{self.id}/">{self}</a>'
            )
 