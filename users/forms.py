from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from mailing.forms import StyleFormMixin
from users.models import User
from django import forms
from django.utils.translation import gettext_lazy as _


class UserAuthenticationForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User


class UserRegistrationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password1', 'password2')


class UserUserChangeForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
