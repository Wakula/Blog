from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from blog_app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home_url'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/',LogoutView.as_view(next_page='home_url'), name='logout_url'),
    path('blog/', views.UserBlogView.as_view(), name='blog_url'),
    path('post/', views.PostCreationView.as_view(), name='post_url'),
]
