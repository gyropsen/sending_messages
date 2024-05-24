from django.urls import path

from blog.apps import BlogConfig
from blog.views import (ArticleCreateView, ArticleDeleteView, ArticleDetailView, ArticleListView, ArticleUpdateView,
                        StartPageTemplateView)

app_name = BlogConfig.name

urlpatterns = [
    # CRUD Blog
    path("", StartPageTemplateView.as_view(), name="start_page"),
    path("blog/", ArticleListView.as_view(), name="article_list"),
    path("blog/article_create/", ArticleCreateView.as_view(), name="article_create"),
    path("blog/article_update/<int:pk>", ArticleUpdateView.as_view(), name="article_update"),
    path("blog/article_detail/<int:pk>", ArticleDetailView.as_view(), name="article_detail"),
    path("blog/article_delete/<int:pk>", ArticleDeleteView.as_view(), name="article_delete"),
]
