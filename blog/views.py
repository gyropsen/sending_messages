from random import shuffle

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from blog.forms import ArticleForm
from blog.models import Article
from data_statistics.models import Client
from mailing.models import Mailing
from mailing.services import model_objects_all


# CRUD статей
class ArticleListView(ListView):
    """
    Представление - это вызываемый объект, который принимает запрос и возвращает ответ
    Представление всех статей
    """

    model = Article
    extra_context = {"title": "Просмотр статей", "description": "Все статьи в блоге"}


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление создания статьи
    """

    model = Article
    form_class = ArticleForm
    permission_required = "blog.add_article"
    extra_context = {"title": "Создание статьи", "description": "Создайте статью для блога"}
    success_url = reverse_lazy("blog:article_list")


class ArticleDetailView(DetailView):
    """
    Представление детального просмотра сообщения
    """

    model = Article
    extra_context = {
        "title": "Просмотр статьи",
        "description": "Эта статья отображается в блоге",
    }

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Представление редактирования сообщения
    """

    model = Article
    form_class = ArticleForm
    permission_required = "blog.change_article"
    extra_context = {
        "title": "Редактирование статьи",
        "description": "Редактируйте статью, которое будет отображается в блоге",
    }

    def get_success_url(self):
        """
        Возвращает url представления детального просмотра сообщения
        :return: Url
        """
        return reverse("blog:article_detail", args=[self.object.pk])


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Представление удаления сообщения
    """

    model = Article
    permission_required = "blog.delete_article"
    success_url = reverse_lazy("blog:article_list")
    extra_context = {"title": "Удаление статьи", "description": "После удаления статью восстановить невозможно"}


class StartPageTemplateView(TemplateView):
    template_name = "blog/start_page.html"
    extra_context = {"title": "SendMes - удобный сервис", "description": "15 минут - и рассылка готова"}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["mailings_all"] = len(model_objects_all(Mailing))
        context_data["mailings_is_active"] = len(Mailing.objects.filter(is_active=True))
        context_data["clients_all"] = len(model_objects_all(Client))
        context_data["article_list"] = Article.objects.order_by("?")
        return context_data
