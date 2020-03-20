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
            return render(request, 'blog_app/index.html')
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
                return render(request, 'blog_app/successfully_created_blog.html')
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


class PostListView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        pass
