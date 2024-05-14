from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    # CHOICES
    DAILY = 'DAY'
    WEEKLY = 'WEEK'
    MONTHLY = 'MONTH'
    PERIODICITY = [
        (DAILY, 'раз в день'), (WEEKLY, 'раз в неделю'), (MONTHLY, 'раз в месяц')
    ]

    CREATED = 'CR'
    LAUNCHED = 'LA'
    COMPLETED = 'CP'
    PAUSED = 'PA'
    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
        (PAUSED, 'Пауза'),
    ]

    # DATABASE FIELDS
    name = models.CharField(max_length=128, verbose_name='Название рассылки', unique=True)
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    time_start = models.TimeField(default=timezone.now, verbose_name='Дата и время старта')
    time_stop = models.TimeField(default=timezone.now, verbose_name='Дата и время окончания')
    periodicity = models.CharField(max_length=8, choices=PERIODICITY, default=MONTHLY, verbose_name='Периодичность')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=CREATED, verbose_name='Статус')

    # META CLASS
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    # TO STRING METHOD
    def __str__(self):
        return str(self.name)


class Message(models.Model):
    # DATABASE FIELDS
    title = models.CharField(max_length=128, unique=True, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    last_used = models.DateField(auto_now=True, verbose_name='Дата последнего использования')
    is_active = models.BooleanField(default=False, verbose_name='Активное сообщение')

    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Активная рассылка")

    # META CLASS
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    # TO STRING METHOD
    def __str__(self):
        return str(self.title)
