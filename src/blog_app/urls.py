from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from blog_app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home_url'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(next_page='home_url'), name='logout_url'),
    path('my_blog/', views.UserBlogView.as_view(), name='my_blog_url'),
    path('posts/', views.PostCreationView.as_view(), name='posts_url'),
    path('blogs/', views.OthersBlogsView.as_view(), name='blogs_url'),
    path('blogs/<int:blog_id>/', views.OthersBlogsView.as_view(), name='single_blog_url'),
    path('posts/<int:post_id>/', views.SinglePostView.as_view(), name='single_post_url')
]
