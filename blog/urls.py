from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleUpdateView, ArticleDetailView, ArticleCreateView, ArticleDeleteView

app_name = BlogConfig.name

urlpatterns = [
    # CRUD Blog
    path("", ArticleListView.as_view(), name="article_list"),
    path("article_create/", ArticleCreateView.as_view(), name="article_create"),
    path("article_update/<int:pk>", ArticleUpdateView.as_view(), name="article_update"),
    path("article_detail/<int:pk>", ArticleDetailView.as_view(), name="article_detail"),
    path("article_delete/<int:pk>", ArticleDeleteView.as_view(), name="article_delete"),
]
