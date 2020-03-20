from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from blog_app.models import Blog, Post
from blog_app.forms import BlogForm, PostForm


class IndexView(View):
    def get(self, request):
        if request.user.is_superuser:
            return redirect('/admin/')
        if request.user.is_authenticated:
            subscribed_blogs = request.user.subscribed_blogs.all()
            posts = []
            for blog in subscribed_blogs:
                posts += list(blog.post_set.all())
            posts.sort(key = lambda blog: blog.date_pub, reverse=True)
            for post in posts:
                post.is_read = post in request.user.read_posts.all()
            return render(request, 'blog_app/index.html', context={'posts': posts})
        return redirect('login_url')


class UserBlogView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        try:
            request.user.blog
        except ObjectDoesNotExist:
            form = BlogForm(request.user)
            return render(request, 'blog_app/blog_create.html', context={'form': form})
        blog = request.user.blog
        posts = Post.objects.filter(blog=blog)
        
        return render(request, 'blog_app/blog_page.html', context={'blog': blog, 'posts': posts})

    def post(self, request):
        try:
            request.user.blog
        except ObjectDoesNotExist:
            bound_form = BlogForm(request.user, request.POST)
            if bound_form.is_valid():
                blog = bound_form.save()
                return redirect('blog_url')
            return render(request, 'blog_app/blog_create.html', context={'form': bound_form})
        return render(request, 'blog_app/blog_already_exists.html')


class BlogListView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'reidrect_to'

    def get(self, request):
        blogs = Blog.objects.exclude(author=request.user)
        for blog in blogs:
            blog.is_subscribed = blog in request.user.subscribed_blogs.all()
        return render(request, 'blog_app/all_blogs.html', context={'blogs': blogs})

    def post(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        if blog.user_is_subscribed(request.user):
            blog.subscribers.remove(request.user)
            user_posts = set(request.user.read_posts.all())
            blog_posts = set(blog.post_set.all())
            read_posts = user_posts.intersection(blog_posts)
            for post in read_posts:
                post.users_that_have_read.remove(request.user)
        else:
            blog.subscribers.add(request.user)
        return redirect('all_blogs_url')
        

class PostCreationView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        form = PostForm(request.user.blog)
        return render(request, 'blog_app/post_create.html', context={'form': form})

    def post(self, request):
            bound_form = PostForm(request.user.blog, request.POST)
            if bound_form.is_valid():
                post = bound_form.save()
                return render(request, 'blog_app/successfully_created_post.html')
            return render(request, 'blog_app/post_create.html', context={'form': bound_form})


class SinglePostView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        return render(request, 'blog_app/read_post.html', context={'post': post})
        
    def post(self, request, post_id):
        read_post = Post.objects.get(id=post_id)
        read_post.users_that_have_read.add(request.user)

        return redirect('home_url')
