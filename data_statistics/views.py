from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from data_statistics.forms import ClientForm
from data_statistics.models import Client, MailingStat
from mailing.models import Mailing
from mailing.utils import AddArgumentsInForms, ControlUserObject


# CRUD Статистики рассылки
class MailingStatListView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, ListView):
    """
    Представление - это вызываемый объект, который принимает запрос и возвращает ответ
    Представление всех статистик рассылок
    """

    model = MailingStat
    permission_required = "data_statistics.view_mailingstat"
    extra_context = {
        "title": "Просмотр попыток рассылки",
        "description": "В таблице отображаются все попытки рассылки",
    }


class MailingStatDetailView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, DetailView):
    """
    Представление детального просмотра статистики рассылки
    """

    model = MailingStat
    permission_required = "data_statistics.view_mailingstat"
    extra_context = {"title": "Просмотр попыток рассылки", "description": "Подробный отчёт по попытке рассылки"}


class MailingStatDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, DeleteView):
    """
    Представление удаления статистики рассылки
    """

    model = MailingStat
    success_url = reverse_lazy("data_statistics:mailing_stat_list")
    permission_required = "data_statistics.delete_mailingstat"
    extra_context = {
        "title": "Удаление попытки рассылки",
        "description": "После удаления попытки рассылки восстановить невозможно",
    }


# CRUD Клиентов
class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, ListView):
    """
    Представление всех клиентов
    """

    model = Client
    permission_required = "data_statistics.view_client"
    extra_context = {
        "title": "Просмотр клиентов рассылки",
        "description": "В таблице отображаются все клиенты рассылки",
    }


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, AddArgumentsInForms, CreateView):
    """
    Представление создания клиента
    """

    model = Client
    form_class = ClientForm
    permission_required = "data_statistics.add_client"
    success_url = reverse_lazy("data_statistics:client_list")
    extra_context = {
        "title": "Создание клиента рассылки",
        "description": "Создайте клиента, которому отправляется рассылка",
    }

    def form_valid(self, form):
        """
        Функция проверки валидности и сохранения формы в базу данных
        :return: HttpResponseRedirect
        """
        object_ = form.save()

        # Присваивание клиенту рассылки
        mailing = Mailing.objects.get(pk=self.request.POST.get("mailing"))
        object_.mailing.add(mailing)

        # Присваивание клиенту пользователя
        object_.owner = self.request.user
        object_.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, DetailView):
    """
    Представление детального просмотра клиента
    """

    model = Client
    permission_required = "data_statistics.view_client"
    extra_context = {
        "title": "Просмотр клиента рассылки",
        "description": "Изучите параметры клиента, которому отправляется рассылка",
    }

    def get_context_data(self, **kwargs):
        """
        Функция добавления в context_data всех рассылок, от которых клиент получает сообщения
        :return: context_data
        """
        context_data = super().get_context_data(**kwargs)
        context_data["mailings"] = ", ".join(mailing.name for mailing in self.object.mailing.all())
        return context_data


class ClientUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, AddArgumentsInForms, UpdateView
):
    """
    Представление редактирования клиента
    """

    model = Client
    form_class = ClientForm
    permission_required = "data_statistics.change_client"
    extra_context = {
        "title": "Редактирование клиента рассылки",
        "description": "Редактируйте параметры клиента, которому отправляется рассылка",
    }

    def get_success_url(self):
        """
        Возвращает url представления детального просмотра рассылки.
        :return: Url
        """
        return reverse("data_statistics:client_detail", args=[self.object.pk])


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, DeleteView):
    """
    Представление удаления клиента
    """

    model = Client
    success_url = reverse_lazy("data_statistics:client_list")
    permission_required = "data_statistics.delete_client"
    extra_context = {
        "title": "Удаление клиента рассылки",
        "description": "После удаления клиента восстановить невозможно",
    }
