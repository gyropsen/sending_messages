from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (MailingCreateView, MailingDeleteView, MailingDetailView, MailingListView, MailingUpdateView,
                           MessageCreateView, MessageDeleteView, MessageDetailView, MessageListView, MessageUpdateView)

app_name = MailingConfig.name

urlpatterns = [
    # CRUD Message
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path("message_detail/<int:pk>", MessageDetailView.as_view(), name="message_detail"),
    path("message_update/<int:pk>", MessageUpdateView.as_view(), name="message_update"),
    path("message_delete/<int:pk>", MessageDeleteView.as_view(), name="message_delete"),
    # CRUD Mailing
    path("", MailingListView.as_view(), name="mailing_list"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing_detail/<int:pk>", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing_update/<int:pk>", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing_delete/<int:pk>", MailingDeleteView.as_view(), name="mailing_delete"),
]
