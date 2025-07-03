from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.management import call_command
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from mailing.forms import MailingForm
from mailing.models import Mailing, MailingAttempt, Message, Recipient
from mailing.services import send_mailing


def main_page(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='running').count()
    unique_clients = Recipient.objects.distinct().count()

    total_attempts = MailingAttempt.objects.count()
    successful_attempts = MailingAttempt.objects.filter(status=True).count()
    failed_attempts = MailingAttempt.objects.filter(status=False).count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'total_attempts': total_attempts,
        'successful_attempts': successful_attempts,
        'failed_attempts': failed_attempts,
    }
    return render(request, 'main.html', context)


def base_view(request):
    return render(request, 'base.html')


def start_mailing_view(request, mailing_id):
    mailing = get_object_or_404(Mailing, pk=mailing_id)

    try:
        call_command('start_mailing', str(mailing_id), 'start')
        messages.success(request, f'Рассылка {mailing.message} успешно запущена.')
    except Exception as e:
        messages.error(request, f'Ошибка при запуске рассылки: {str(e)}')

    return redirect('mailing:mailing_detail', pk=mailing_id)


@login_required
@permission_required('mailing.can_complete_mailing')
def complete_mailing_view(request, mailing_id):
    mailing = get_object_or_404(Mailing, pk=mailing_id)

    try:
        call_command('start_mailing', str(mailing_id), 'complete')
        messages.success(request, f'Рассылка {mailing.message} успешно завершена.')
    except Exception as e:
        messages.error(request, f'Ошибка при завершении рассылки: {str(e)}')

    return redirect('mailing:mailing_detail', pk=mailing_id)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['subject_letter', 'body_letter']
    template_name = 'message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = context['messages']

        for message in messages:
            message.can_change = (message.user == self.request.user or
                                  self.request.user.has_perm("mailing.change_message"))

        context['messages'] = messages
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['subject_letter', 'body_letter']
    template_name = 'message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    fields = ['email', 'name', 'comment']
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipients = context['recipients']

        for recipient in recipients:
            recipient.can_change = (recipient.user == self.request.user or
                                    self.request.user.has_perm("mailing.change_recipient"))
        context['recipients'] = recipients
        return context


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'recipient_detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    fields = ['email', 'name', 'comment']
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = context['mailings']

        for mailing in mailings:
            mailing.can_change = (mailing.user == self.request.user or
                                  self.request.user.has_perm("mailing.change_mailing"))

        context['mailings'] = mailings
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        send_mailing(obj)
        return obj


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


@permission_required("mailing.can_disable_mailing")
def disable_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, pk=mailing_id)
    mailing.is_active = False
    mailing.save()
    return redirect('mailing:mailing_list')
