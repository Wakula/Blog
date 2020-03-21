from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from blog_app.models import Blog, Post, BlogUser
from blog_app.forms import BlogForm, PostForm


class IndexView(View):
    def get(self, request):
        if request.user.is_superuser:
            return redirect('/admin/')
        if request.user.is_authenticated:
            blog_user = BlogUser.objects.get(username=request.user.username)
            news_line = blog_user.get_news_line()
            return render(request, 'blog_app/index.html', context={'posts': news_line})
        return redirect('login_url')


class UserBlogView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        try:
            request.user.blog
        except ObjectDoesNotExist:
            form = BlogForm(request.user)
            return render(request, 'blog_app/blog_declaration.html', context={'form': form})
        blog = request.user.blog
        posts = Post.objects.filter(blog=blog)

        return render(request, 'blog_app/my_blog.html', context={'blog': blog, 'posts': posts})

    def post(self, request):
        try:
            request.user.blog
        except ObjectDoesNotExist:
            bound_form = BlogForm(request.user, request.POST)
            if bound_form.is_valid():
                bound_form.save()
                return redirect('my_blog_url')
            return render(request, 'blog_app/blog_declaration.html', context={'form': bound_form})
        return render(request, 'blog_app/blog_exists.html')


class OthersBlogsView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'reidrect_to'

    def get(self, request):
        blogs = Blog.objects.get_other_users_blogs(request.user)
        return render(request, 'blog_app/others_blogs.html', context={'blogs': blogs})

    def post(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        if blog.user_is_subscribed(request.user):
            blog.unsubscribe(request.user)
        else:
            blog.subscribe(request.user)
        return redirect('blogs_url')


class PostCreationView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        form = PostForm(request.user.blog)
        return render(request, 'blog_app/post_declaration.html', context={'form': form})

    def post(self, request):
        bound_form = PostForm(request.user.blog, request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return render(request, 'blog_app/post_created.html')
        return render(request, 'blog_app/post_declaration.html', context={'form': bound_form})


class SinglePostView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        return render(request, 'blog_app/post_detailed.html', context={'post': post})

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post.mark_as_read(request.user)

        return redirect('home_url')
