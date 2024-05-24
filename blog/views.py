from blog.models import Article
from blog.forms import ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin


# CRUD статей
class ArticleListView(LoginRequiredMixin, ListView):
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


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """
    Представление детального просмотра сообщения
    """

    model = Article
    extra_context = {
        "title": "Просмотр статьи",
        "description": "Эта статья отображается в блоге",
    }


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
