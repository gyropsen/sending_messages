from django.db import models

from mailing.models import NULLABLE


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(**NULLABLE, verbose_name="Содержимое")
    image = models.ImageField(**NULLABLE, upload_to="blog/", verbose_name="Превью")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    views_count = models.IntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
