from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory, modelformset_factory
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from data_statistics.forms import ClientForm
from data_statistics.models import Client
from mailing.forms import MailingForm, MessageForm
from mailing.models import Mailing, Message
from mailing.utils import AddArgumentsInForms, ControlUserObject


# CRUD сообщений
class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, ListView):
    """
    Представление - это вызываемый объект, который принимает запрос и возвращает ответ
    Представление всех сообщений
    """

    model = Message
    permission_required = "mailing.view_message"
    extra_context = {"title": "Просмотр сообщений", "description": "В таблице отображаются все сообщения"}


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, AddArgumentsInForms, CreateView):
    """
    Представление создания сообщения
    """

    model = Message
    form_class = MessageForm
    permission_required = "mailing.add_message"
    extra_context = {
        "title": "Создание сообщения",
        "description": "Создайте сообщение, которое будет использоваться в рассылке",
    }
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        """
        Функция проверки валидности и сохранения формы в базу данных
        """
        object_ = form.save()
        object_.owner = self.request.user
        object_.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, DetailView):
    """
    Представление детального просмотра сообщения
    """

    model = Message
    permission_required = "mailing.view_message"
    extra_context = {
        "title": "Просмотр сообщения",
        "description": "Изучите параметры сообщения, которое будет отправляется вашим клиентам",
    }


class MessageUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, AddArgumentsInForms, UpdateView
):
    """
    Представление редактирования сообщения
    """

    model = Message
    form_class = MessageForm
    permission_required = "mailing.change_message"
    extra_context = {
        "title": "Редактирование сообщения",
        "description": "Редактируйте сообщение, которое будет использоваться в рассылке",
    }

    def get_success_url(self):
        """
        Возвращает url представления детального просмотра сообщения
        :return: Url
        """
        return reverse("mailing:message_detail", args=[self.object.pk])


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, DeleteView):
    """
    Представление удаления сообщения
    """

    model = Message
    permission_required = "mailing.delete_message"
    success_url = reverse_lazy("mailing:message_list")
    extra_context = {"title": "Удаление сообщения", "description": "После удаления сообщение восстановить невозможно"}


# CRUD рассылок
class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, ListView):
    """
    Представление просмотра всех рассылок
    """

    model = Mailing
    permission_required = "mailing.view_mailing"
    extra_context = {"title": "Просмотр рассылок", "description": "В таблице отображаются все рассылки"}


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление создания рассылки
    """

    model = Mailing
    form_class = MailingForm
    permission_required = "mailing.add_mailing"
    extra_context = {
        "title": "Создание рассылки",
        "description": "Создайте рассылку, которая будет отправлять сообщения клиентам",
    }
    success_url = reverse_lazy("mailing:mailing_list")

    def get_context_data(self, **kwargs):
        """
        Вместе с созданием рассылки, можно создать и сообщения путем создания формсета сообщений.
        :return: Context_data
        """
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1)

        # В зависимости от метода передаем в формсет данные на сохранение
        if self.request.method == "POST":
            message_formset = MessageFormset(self.request.POST, instance=self.object)
        else:
            message_formset = MessageFormset(instance=self.object)

        context_data["message_formset"] = message_formset
        return context_data

    def form_valid(self, form):
        """
        Функция проверки валидности и сохранения формы и формсетов в базу данных
        :return: HttpResponseRedirect
        """
        context_data = self.get_context_data()
        message_formset = context_data["message_formset"]

        object_ = form.save()
        object_.owner = self.request.user
        object_.save()

        if message_formset.is_valid():
            message_formset.instance = object_
            message_formset.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, DetailView):
    """
    Представление детального просмотра рассылки
    """

    model = Mailing
    permission_required = "mailing.detail_mailing"
    extra_context = {
        "title": "Просмотр рассылки",
        "description": "Изучите параметры рассылки, которая будет отправлена вашим клиентам",
    }

    def get_context_data(self, **kwargs):
        """
        Вместе с детальным просмотром рассылки, можно просмотреть сообщения и клиентов рассылки
        :return: Context_data
        """
        context_data = super().get_context_data(**kwargs)

        # Получение данных рассылки
        messages = Message.objects.filter(mailing=self.object).filter(is_active=True)
        clients = [client for client in self.object.client_set.all()]

        context_data["message"] = messages[0] if messages else None
        context_data["client_list"] = clients
        return context_data


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, UpdateView):
    """
    Представление редактирования рассылки
    """

    model = Mailing
    form_class = MailingForm
    permission_required = "mailing.change_mailing"
    extra_context = {
        "title": "Редактирование рассылки",
        "description": "Редактируйте рассылку, которая будет отправлена вашим клиентам",
    }

    def get_context_data(self, **kwargs):
        """
        Вместе с редактированием рассылки, можно редактировать сообщения и клиентов рассылки
        путем создания формсетов
        :param kwargs:
        :return: Context_data
        """
        context_data = super().get_context_data(**kwargs)

        # Создать формсеты
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1)
        ClientFormset = modelformset_factory(Client, form=ClientForm, extra=1)

        # Если POST - сохраняем данные, иначе пустая форма
        if self.request.method == "POST":
            message_formset = MessageFormset(self.request.POST, instance=self.object)
            client_formset = ClientFormset(self.request.POST)
        else:
            message_formset = MessageFormset(instance=self.object, form_kwargs={"user": self.request.user})
            client_formset = ClientFormset(
                queryset=Client.objects.filter(owner=self.request.user), form_kwargs={"user": self.request.user}
            )

        context_data["message_formset"] = message_formset
        context_data["client_formset"] = client_formset
        return context_data

    def get_success_url(self):
        """
        Возвращает url представления детального просмотра рассылки.
        :return: Url
        """
        return reverse("mailing:mailing_detail", args=[self.object.pk])

    def form_valid(self, form):
        """
        Функция проверки валидности и сохранения формы и формсетов в базу данных
        :return: HttpResponseRedirect
        """
        context_data = self.get_context_data()
        message_formset = context_data["message_formset"]
        client_formset = context_data["client_formset"]
        object_ = form.save()

        if message_formset.is_valid() and client_formset.is_valid():
            message_formset.instance = object_
            client_formset.instance = object_

            message_formset.save()
            client_formset.save()
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ControlUserObject, DeleteView):
    """
    Представление удаления рассылки
    """

    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")
    permission_required = "mailing.delete_mailing"
    extra_context = {"title": "Удаление рассылки", "description": "После удаления рассылку восстановить невозможно"}
