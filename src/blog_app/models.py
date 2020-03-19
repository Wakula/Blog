from django.db import models
from django.contrib.auth import get_user_model


class Blog(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(get_user_model(), blank=True, related_name='subscribed_blogs')

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    users_that_have_read = models.ManyToManyField(get_user_model(), blank=True, related_name='read_posts')

    def __str__(self):
        return f'{self.title}'
