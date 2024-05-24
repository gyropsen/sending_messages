from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "content",
        "created_at",
        "views_count",
    )
    search_fields = (
        "title",
        "content",
    )
    ordering = ("pk",)
