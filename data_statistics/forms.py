from django import forms

from data_statistics.models import Client
from mailing.utils import ConfigForms, GetArgumentsInForms


class ClientForm(ConfigForms, GetArgumentsInForms, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("owner",)

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
