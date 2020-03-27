from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from blog_app.tasks import email_task


# class BlogUser(User):
#     class Meta:
#         proxy = True

#     def get_news_line(self):
#         subscribed_blogs = self.subscribed_blogs.all()
#         posts = []
#         for blog in subscribed_blogs:
#             posts += list(blog.post_set.all())
#         posts.sort(key=lambda blog: blog.date_pub, reverse=True)
#         for post in posts:
#             post.is_read = post in self.read_posts.all()
#         return posts


# class BlogManager(models.Manager):
#     def get_other_users_blogs(self, user):
#         blogs = self.exclude(author=user)
#         for blog in blogs:
#             blog.is_subscribed = blog in user.subscribed_blogs.all()
#         return blogs


class Profile(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField()
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='subscribed_blogs')
    objects = BlogManager()

    def user_is_subscribed(self, user):
        return user in self.subscribers.all()

    def subscribe(self, user):
        self.subscribers.add(user)

    def unsubscribe(self, user):
        self.subscribers.remove(user)
        user_posts = set(user.read_posts.all())
        blog_posts = set(self.post_set.all())
        read_posts = user_posts.intersection(blog_posts)
        for post in read_posts:
            post.users_that_have_read.remove(user)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    users_that_have_read = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='read_posts')

    def mark_as_read(self, user):
        self.users_that_have_read.add(user)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in self.blog.subscribers.all():
            email_task.delay(self.title, self.blog.name, self.id, user.email)
