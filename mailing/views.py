from django.shortcuts import render
from mailing.models import Mailing, Message
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse


class MessageListView(ListView):
    model = Message
    extra_context = {'title': 'Просмотр сообщений',
                     'description': 'В таблице отображаются все сообщения'}


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'body', 'mailing')
    extra_context = {'title': 'Создание сообщения',
                     'description': 'Создайте сообщение, которое будет использоваться в рассылке'}
    success_url = reverse_lazy('mailing:message_list')


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'body', 'mailing')
    extra_context = {'title': 'Редактирование сообщения',
                     'description': 'Редактируйте сообщение, которое будет использоваться в рассылке'}

    def get_success_url(self):
        return reverse('mailing:message_detail', args=[self.object.pk])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MailingListView(ListView):
    model = Mailing
    extra_context = {"title": 'Просмотр рассылок', 'description': "В таблице отображаются все рассылки"}


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('name', 'datetime_start', 'datetime_stop', 'periodicity',)
    extra_context = {'title': 'Создание рассылки',
                     'description': 'Создайте рассылку, которая будет отправлять сообщения клиентам'}
    success_url = reverse_lazy('mailing:mailing_list')
