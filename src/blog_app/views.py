from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from blog_app.models import Blog, Post
from blog_app.forms import BlogForm


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
            return render(request, 'blog_app/blog_create.html', context={'form': bound_form})
        return render(request, 'blog_app/blog_already_exists.html')

class BlogListView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'reidrect_to'

    def get(self, request):
        pass


class SinglePostView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        pass

    def post(self, request):
        pass


class PostListView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        pass
