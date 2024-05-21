from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from mailing.forms import ForbiddenWordsMixin, StyleFormMixin
from users.models import User


class CleanUser(ForbiddenWordsMixin):
    """
    Класс проверки форм пользователя на запрещённые слова
    """

    def clean_name(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["name"]
        for word in cleaned_data.lower().split(" "):
            if word in CleanUser.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {word}.")
        return cleaned_data

    def clean_surname(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["surname"]
        for word in cleaned_data.lower().split(" "):
            if word in CleanUser.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {word}.")
        return cleaned_data


class UserAuthenticationForm(StyleFormMixin, AuthenticationForm):
    """
    Класс формы аутентификации пользователей
    """

    class Meta:
        model = User


class UserRegistrationForm(StyleFormMixin, CleanUser, UserCreationForm):
    """
    Класс формы регистрации пользователей
    """

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password1", "password2")


class UserUserChangeForm(StyleFormMixin, CleanUser, UserChangeForm):
    """
    Класс формы редактирования пользователей
    """

    class Meta:
        model = User
        fields = ("name", "surname", "email", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
