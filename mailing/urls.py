from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, \
    MessageDeleteView, MailingListView, MailingCreateView

app_name = MailingConfig.name

urlpatterns = [
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('', MailingListView.as_view(), name='mailing_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),

]
