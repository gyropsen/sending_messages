from django.shortcuts import render

from mailing.forms import MessageForm, MailingForm
from mailing.models import Mailing, Message
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse


class MessageListView(ListView):
    model = Message
    extra_context = {'title': 'Просмотр сообщений',
                     'description': 'В таблице отображаются все сообщения'}


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Создание сообщения',
                     'description': 'Создайте сообщение, которое будет использоваться в рассылке'}
    success_url = reverse_lazy('mailing:message_list')


class MessageDetailView(DetailView):
    model = Message
    extra_context = {'title': 'Просмотр сообщения',
                     'description': 'Изучите параметры сообщения, которое будет отправляется вашим клиентам'}


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Редактирование сообщения',
                     'description': 'Редактируйте сообщение, которое будет использоваться в рассылке'}

    def get_success_url(self):
        return reverse('mailing:message_detail', args=[self.object.pk])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    extra_context = {"title": 'Удаление сообщения',
                     'description': "После удаления сообщение восстановить невозможно"}


class MailingListView(ListView):
    model = Mailing
    extra_context = {"title": 'Просмотр рассылок',
                     'description': "В таблице отображаются все рассылки"}


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Создание рассылки',
                     'description': 'Создайте рассылку, которая будет отправлять сообщения клиентам'}
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDetailView(DetailView):
    model = Mailing
    extra_context = {'title': 'Просмотр рассылки',
                     'description': 'Изучите параметры рассылки, которая будет отправлена вашим клиентам'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)


class MailingUpdateView(UpdateView):
    model = Mailingv
    form_class = MailingForm
    extra_context = {'title': 'Редактирование рассылки',
                     'description': 'Редактируйте рассылку, которая будет отправлена вашим клиентам'}

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.object.pk])

v
class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {"title": 'Удаление рассылки',
                     'description': "После удаления рассылку восстановить невозможно"}
