from django.urls import path

from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    # Базовый функционал пользователя
    # path("login/", Login.as_view(), name="login"),
    # path("logout/", Logout.as_view(), name="logout"),
]
