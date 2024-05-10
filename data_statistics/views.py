from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from data_statistics.models import Client, MailingStat
from django.urls import reverse_lazy
from data_statistics.forms import ClientForm
from mailing.models import Mailing
from django.urls import reverse


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

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context_data = super().get_context_data(object_list=None, **kwargs)
    #
    #     print(self.object_list[0].mailing)
    #     return context_data


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('data_statistics:client_list')
    extra_context = {'title': 'Создание клиента рассылки',
                     'description': 'Создайте клиента, которому отправляется рассылка'}

    def form_valid(self, form):
        client = form.save()
        mailing = Mailing.objects.get(pk=self.request.POST.get('mailing'))
        client.mailing.add(mailing)
        return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client
    extra_context = {'title': 'Просмотр клиента рассылки',
                     'description': 'Изучите параметры клиента, которому отправляется рассылка'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailings'] = ", ".join(mailing.name for mailing in self.object.mailing.all())
        return context_data


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {'title': 'Редактирование клиента рассылки',
                     'description': 'Редактируйте параметры клиента, которому отправляется рассылка'}

    def get_success_url(self):
        return reverse('data_statistics:client_detail', args=[self.object.pk])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('data_statistics:client_list')
    extra_context = {'title': 'Удаление клиента рассылки',
                     'description': 'После удаления клиента восстановить невозможно'}
