from django.forms import inlineformset_factory, formset_factory, modelform_factory
from mailing.forms import MessageForm, MailingForm
from mailing.models import Mailing, Message
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import FullResultSet


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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1)
        # ClientFormset = inlineformset_factory(Mailing, Message, form=ClientForm, extra=1)
        if self.request.method == "POST":
            message_formset = MessageFormset(self.request.POST, instance=self.object)
            # client_formset = ClientFormset(self.request.POST, instance=self.object)
        else:
            message_formset = MessageFormset(instance=self.object)
            # client_formset = ClientFormset(instance=self.object)
        context_data['message_formset'] = message_formset
        # context_data['client_formset'] = client_formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        message_formset = context_data['message_formset']
        object_ = form.save()

        if message_formset.is_valid():
            message_formset.instance = object_
            message_formset.save()
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing
    extra_context = {'title': 'Просмотр рассылки',
                     'description': 'Изучите параметры рассылки, которая будет отправлена вашим клиентам'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        messages = Message.objects.filter(mailing=self.object)
        if messages:
            for message in messages:
                if message.is_active is False:
                    active_message = None
                else:
                    active_message = message
                    break
        else:
            active_message = None
        context_data['message'] = active_message
        return context_data


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Редактирование рассылки',
                     'description': 'Редактируйте рассылку, которая будет отправлена вашим клиентам'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1)
        # ClientFormset = inlineformset_factory(Mailing, Message, form=ClientForm, extra=1)
        if self.request.method == "POST":
            message_formset = MessageFormset(self.request.POST, instance=self.object)
            # client_formset = ClientFormset(self.request.POST, instance=self.object)
        else:
            message_formset = MessageFormset(instance=self.object)
            # client_formset = ClientFormset(instance=self.object)
        context_data['message_formset'] = message_formset
        # context_data['client_formset'] = client_formset
        return context_data

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.object.pk])

    def form_valid(self, form):
        context_data = self.get_context_data()
        message_formset = context_data['message_formset']
        object_ = form.save()

        if message_formset.is_valid():
            message_formset.instance = object_
            message_formset.save()
        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {"title": 'Удаление рассылки',
                     'description': "После удаления рассылку восстановить невозможно"}
