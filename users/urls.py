from django.urls import path
from users.apps import UsersConfig
from users.views import Login, Logout, UserRegisterView, UserUpdateView, email_confirm, success_email_confirm

app_name = UsersConfig.name

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),

    path('email_confirm/<str:email>', email_confirm, name='email_confirm'),
    path('success_email_confirm/<str:token>/', success_email_confirm, name='success_email_confirm'),
]
