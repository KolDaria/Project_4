from django.urls import include, path

from mailing.apps import MailingConfig
from mailing.views import (MailingAttemptListView, MailingCreateView, MailingDeleteView, MailingDetailView,
                           MailingListView, MailingUpdateView, MessageCreateView, MessageDeleteView, MessageDetailView,
                           MessageListView, MessageUpdateView, RecipientCreateView, RecipientDeleteView,
                           RecipientDetailView, RecipientListView, RecipientUpdateView, complete_mailing_view,
                           main_page, send_mailing_view, start_mailing_view)

app_name = MailingConfig.name

urlpatterns = [
    path('', main_page, name='main'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/new/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('recipient/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/new/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/<int:pk>/edit/', RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipient/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/new/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/<int:mailing_id>/start/', start_mailing_view, name='start_mailing'),
    path('mailing/<int:mailing_id>/complete/', complete_mailing_view, name='complete_mailing'),
    path('mailing/<int:mailing_id>/send/', send_mailing_view, name='send_mailing'),
    path('attempts/', MailingAttemptListView.as_view(), name='mailing_attempt_list'),
    path('users/<int:user_id>/toggle/', include('users.urls')),
]
