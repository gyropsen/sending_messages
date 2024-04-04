from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    # DATABASE FIELDS
    name = models.CharField(max_length=64, verbose_name='Имя')
    surname = models.CharField(max_length=64, verbose_name='Фамилия')
    email = models.EmailField(max_length=64, unique=True, verbose_name='Адрес электронной почты')
    comment = models.CharField(max_length=128, **NULLABLE, verbose_name='Комментарий')

    # META CLASS
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    # TO STRING METHOD
    def __str__(self):
        return f'{self.name} {self.surname} ({self.email})'


class MailingStat(models.Model):
    # DATABASE FIELDS
    name = models.CharField(max_length=128, verbose_name='Название статистики рассылки')
    attempt_datetime = models.DateTimeField(verbose_name='Дата и время последней попытки')
    status_attempt = models.BooleanField(default=False, verbose_name='Статус попытки')
    response = models.CharField(max_length=128, verbose_name='Ответ почтового сервера')

    # META CLASS
    class Meta:
        verbose_name = 'Статистика Email рассылки'
        verbose_name_plural = 'Статистики Email рассылки'

    # TO STRING METHOD
    def __str__(self):
        return str(self.name)
