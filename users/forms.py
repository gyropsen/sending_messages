from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from users.models import User
from users.utils import CleanUser


class UserAuthenticationForm(AuthenticationForm):
    """
    Класс формы аутентификации пользователей
    """

    class Meta:
        model = User


class UserRegistrationForm(CleanUser, UserCreationForm):
    """
    Класс формы регистрации пользователей
    """

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password1", "password2")


class UserUserChangeForm(CleanUser, UserChangeForm):
    """
    Класс формы редактирования пользователей
    """

    class Meta:
        model = User
        fields = ("name", "surname", "email", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
