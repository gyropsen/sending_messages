from django.db import models

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
    name = models.CharField(max_length=128, verbose_name='Название рассылки')
    last_used = models.DateField(auto_now=True, verbose_name='Дата последнего использования')
    periodicity = models.CharField(max_length=8, choices=PERIODICITY, verbose_name='Периодичность')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=CREATED, verbose_name='Статус')
    owner = models.ForeignKey('data_statistics.Owner', on_delete=models.CASCADE, verbose_name='Владелец рассылки')
    clients = models.ManyToManyField('data_statistics.Client', **NULLABLE, verbose_name='Клиент рассылки')

    # META CLASS
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    # TO STRING METHOD
    def __str__(self):
        return str(self.name)


class Message(models.Model):
    # DATABASE FIELDS
    title = models.CharField(max_length=128, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    last_used = models.DateField(auto_now=True, verbose_name='Дата последнего использования')
    mailing = models.OneToOneField(Mailing, on_delete=models.CASCADE)

    # META CLASS
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    # TO STRING METHOD
    def __str__(self):
        return str(self.title)
