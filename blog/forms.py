from django import forms

from blog.models import Article
from mailing.utils import ConfigForms


class ArticleForm(ConfigForms, forms.ModelForm):
    """
    Форма сообщения
    """

    class Meta:
        model = Article
        exclude = ("views_count", "created_at")

    def clean_title(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["title"]
        for word in cleaned_data.lower().split(" "):
            if word in ArticleForm.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {word}.")
        return cleaned_data

    def clean_content(self):
        """
        Функция проверки на запрещенные слова
        """
        cleaned_data = self.cleaned_data["content"]
        for word in cleaned_data.lower().split(" "):
            if word in ArticleForm.forbidden_words:
                raise forms.ValidationError(f"Содержит запрещенное слово: {word}.")
        return cleaned_data
