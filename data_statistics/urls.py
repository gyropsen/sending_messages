from django.urls import path
from data_statistics.apps import DataStatisticsConfig
from data_statistics.views import MailingStatListView, MailingStatDetailView, MailingStatDeleteView, \
    ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = DataStatisticsConfig.name

urlpatterns = [
    path('', MailingStatListView.as_view(), name='mailing_stat_list'),
    # path('mailing_stat_create/', MailingStatCreateView.as_view(), name='mailing_stat_create'),
    path('mailing_stat_detail/<int:pk>', MailingStatDetailView.as_view(), name='mailing_stat_detail'),
    # path('mailing_stat_update/<int:pk>', MailingStatUpdateView.as_view(), name='mailing_stat_update'),
    path('mailing_stat_delete/<int:pk>', MailingStatDeleteView.as_view(), name='mailing_stat_delete'),

    path('client_list', ClientListView.as_view(), name='client_list'),
    path('client_create', ClientCreateView.as_view(), name='client_create'),
    path('mailing_stat_detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('mailing_stat_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('mailing_stat_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
]
