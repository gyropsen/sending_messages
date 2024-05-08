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
        fields = '__all__'


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('status',)
        widgets = {
            'datetime_start': forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date and time',
                       'type': 'datetime-local'}
            ),
            'datetime_stop': forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date and time',
                       'type': 'datetime-local'}
            )
        }
