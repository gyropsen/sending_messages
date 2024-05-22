from django import forms

from mailing.models import Mailing, Message
from mailing.utils import ConfigForms, GetArgumentsInForms


class MessageForm(ConfigForms, GetArgumentsInForms, forms.ModelForm):
    """
    Форма сообщения
    """

    class Meta:
        model = Message
        exclude = ("owner",)

    def clean_title(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["title"]
        for word in cleaned_data.lower().split(" "):
            if word in MessageForm.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {word}.")
        return cleaned_data

    def clean_body(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["body"]
        for word in cleaned_data.lower().split(" "):
            if word in MessageForm.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {word}.")
        return cleaned_data


class MailingForm(ConfigForms, forms.ModelForm):
    """
    Форма рассылки
    """

    class Meta:
        model = Mailing
        exclude = ("status", "owner")
        widgets = {
            "time_start": forms.TimeInput(
                format="%H:%M:%S", attrs={"class": "form-control", "placeholder": "Select a time", "type": "time"}
            ),
            "time_stop": forms.TimeInput(
                format="%H:%M:%S", attrs={"class": "form-control", "placeholder": "Select a time", "type": "time"}
            ),
        }

    def clean_name(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["name"]
        for word in cleaned_data.lower().split(" "):
            if word in MailingForm.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {cleaned_data}.")
        return cleaned_data

    def clean(self):
        """
        Функция проверки на корректность указания времени
        """
        cleaned_data = super().clean()
        time_start = cleaned_data.get("time_start")
        time_stop = cleaned_data.get("time_stop")

        if time_start >= time_stop:
            raise forms.ValidationError("Время старта больше или равно времени окончания")
