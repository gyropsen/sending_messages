from django.contrib import admin

from mailing.models import Message, Mailing


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'last_used', 'mailing',)
    search_fields = ('title', 'body')
    ordering = ('last_used',)
    list_filter = ('mailing',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime_start', 'datetime_stop', 'periodicity', 'status',)
    search_fields = ('name',)
    list_filter = ('status', 'periodicity',)
