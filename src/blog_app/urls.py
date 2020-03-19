from django.urls import path
from django.contrib.auth.views import LoginView
from blog_app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login_url'),
    # path('logout/',),
]
