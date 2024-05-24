from django.urls import path

from data_statistics.apps import DataStatisticsConfig
from data_statistics.views import (ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView,
                                   ClientUpdateView, MailingStatDeleteView, MailingStatDetailView, MailingStatListView)

app_name = DataStatisticsConfig.name

urlpatterns = [
    # CRUD MailingStat
    path("", MailingStatListView.as_view(), name="mailing_stat_list"),
    path("mailing_stat_detail/<int:pk>", MailingStatDetailView.as_view(), name="mailing_stat_detail"),
    path("mailing_stat_delete/<int:pk>", MailingStatDeleteView.as_view(), name="mailing_stat_delete"),
    # CRUD Client
    path("client_list", ClientListView.as_view(), name="client_list"),
    path("client_create", ClientCreateView.as_view(), name="client_create"),
    path("client_detail/<int:pk>", ClientDetailView.as_view(), name="client_detail"),
    path("client_update/<int:pk>", ClientUpdateView.as_view(), name="client_update"),
    path("client_delete/<int:pk>", ClientDeleteView.as_view(), name="client_delete"),
]
