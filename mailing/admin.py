from django.contrib import admin

from mailing.models import Message, Mailing


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'last_used')
    search_fields = ('title', 'body')
    ordering = ('last_used',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_use', 'periodicity', 'status',)
    search_fields = ('name',)
