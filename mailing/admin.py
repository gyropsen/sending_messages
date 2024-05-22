from django.contrib import admin

from mailing.models import Mailing, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "body",
        "last_used",
        "mailing",
    )
    search_fields = ("title", "body")
    ordering = ("last_used",)
    list_filter = ("mailing",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "time_start",
        "time_stop",
        "periodicity",
        "status",
    )
    search_fields = ("name",)
    list_filter = (
        "status",
        "periodicity",
    )
