from django.contrib import admin

from data_statistics.models import Client, MailingStat


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'comment',)
    search_fields = ('name', 'surname', 'email', 'comment',)
    ordering = ('email',)
    list_filter = ('comment',)


@admin.register(MailingStat)
class MailingStatAdmin(admin.ModelAdmin):
    list_display = ('name', 'status_attempt', 'attempt_datetime', 'mailing')
    search_fields = ('name', 'attempt_datetime')
    list_filter = ('status_attempt', 'response', 'mailing')
    ordering = ('attempt_datetime',)
