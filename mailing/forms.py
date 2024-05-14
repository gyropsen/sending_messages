from django import forms
from mailing.models import Mailing, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('status',)
        widgets = {
            'time_start': forms.TimeInput(
                format="%H:%M:%S",
                attrs={'class': 'form-control',
                       'placeholder': 'Select a time',
                       'type': 'time'}
            ),
            'time_stop': forms.TimeInput(
                format="%H:%M:%S",
                attrs={'class': 'form-control',
                       'placeholder': 'Select a time',
                       'type': 'time'}
            )
        }
