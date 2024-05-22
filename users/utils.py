from django import forms

from mailing.utils import ConfigForms


class CleanUser(ConfigForms):
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
