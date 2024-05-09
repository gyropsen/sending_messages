from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from data_statistics.models import Client, MailingStat
from django.urls import reverse_lazy


# Интерфейс для просмотра статистики рассылок
class MailingStatListView(ListView):
    model = MailingStat
    extra_context = {'title': 'Просмотр попыток рассылки',
                     'description': 'В таблице отображаются все попытки рассылки'}


class MailingStatDetailView(DetailView):
    model = MailingStat
    extra_context = {'title': 'Просмотр попыток рассылки',
                     'description': 'Подробный отчёт по попытке рассылки'}


class MailingStatDeleteView(DeleteView):
    model = MailingStat
    success_url = reverse_lazy('data_statistics:mailing_stat_list')
    extra_context = {'title': 'Удаление попытки рассылки',
                     'description': 'После удаления попытки рассылки восстановить невозможно'}


# Интерфейс для просмотра клиентов рассылки
class ClientListView(ListView):
    model = Client
    extra_context = {'title': 'Просмотр клиентов рассылки',
                     'description': 'В таблице отображаются все клиенты рассылки'}


class ClientCreateView(CreateView):
    model = Client
    extra_context = {'title': 'Создание клиента рассылки',
                     'description': 'Создайте клиента, которому отправляется рассылка'}


class ClientDetailView(DetailView):
    model = Client
    extra_context = {'title': 'Просмотр клиента рассылки',
                     'description': 'Изучите параметры клиента, которому отправляется рассылка'}


class ClientUpdateView(UpdateView):
    model = Client
    extra_context = {'title': 'Редактирование клиента рассылки',
                     'description': 'Редактируйте параметры клиента, которому отправляется рассылка'}


class ClientDeleteView(DeleteView):
    model = Client
    extra_context = {'title': 'Удаление клиента рассылки',
                     'description': 'После удаления клиента восстановить невозможно'}
