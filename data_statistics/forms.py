from django import forms
from data_statistics.models import Client
from mailing.forms import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
