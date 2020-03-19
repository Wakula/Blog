from django.shortcuts import render, redirect
from django.views.generic import View


class IndexView(View):
    def get(self, request):
        if request.user.is_superuser:
            return redirect('/admin/')
        if request.user.is_authenticated:
            return render(request, 'blog_app/index.html')
        return redirect('login_url')
