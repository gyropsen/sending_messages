from django import forms

from mailing.models import Mailing, Message


class ForbiddenWordsMixin:
    """
    Миксин для указания запрещённых слов
    """

    forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


class StyleFormMixin:
    """
    Миксин для контроля стилей формы
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "is_active":
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MessageForm(StyleFormMixin, ForbiddenWordsMixin, forms.ModelForm):
    """
    Форма сообщения
    """
    mailing = forms.ModelChoiceField(queryset=Mailing.objects.none())

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['mailing'].queryset = Mailing.objects.filter(owner=user)

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


class MailingForm(StyleFormMixin, ForbiddenWordsMixin, forms.ModelForm):
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
