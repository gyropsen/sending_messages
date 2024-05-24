from django.urls import path

from users.apps import UsersConfig
from users.views import (Login, Logout, UserListView, UserRegisterView, UserUpdateView, email_confirm,
                         mailing_set_active, success_email_confirm, user_set_active)

app_name = UsersConfig.name

urlpatterns = [
    # Базовый функционал пользователя
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/", UserUpdateView.as_view(), name="profile"),
    # Активация посредством подтверждения электронной почты
    path("email_confirm/<str:email>", email_confirm, name="email_confirm"),
    path("success_email_confirm/<str:token>/", success_email_confirm, name="success_email_confirm"),
    # Просмотр, активации
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user_set_active/<int:pk>", user_set_active, name="user_set_active"),
    path("mailing_set_active/<int:pk>", mailing_set_active, name="mailing_set_active"),
]
