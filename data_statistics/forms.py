from django import forms

from data_statistics.models import Client
from mailing.forms import ForbiddenWordsMixin, StyleFormMixin


class ClientForm(StyleFormMixin, ForbiddenWordsMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"

    def clean_comment(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["comment"]
        for word in cleaned_data.lower().split(" "):
            if word in ClientForm.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {word}.")
        return cleaned_data

    def clean_name(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["name"]
        for word in cleaned_data.lower().split(" "):
            if word in ClientForm.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {word}.")
        return cleaned_data

    def clean_surname(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["surname"]
        for word in cleaned_data.lower().split(" "):
            if word in ClientForm.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {word}.")
        return cleaned_data
