from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from mailing.forms import StyleFormMixin
from users.models import User


class UserAuthenticationForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User


class UserRegistrationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("name", "surname", "email", "password1", "password2")


class UserUserChangeForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ("name", "surname", "email", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
