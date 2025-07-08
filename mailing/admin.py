from django.contrib import admin

from .models import Mailing, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'user')  # Отображаемые поля в списке
    list_filter = ('user',)  # Фильтры
    search_fields = ('email', 'name')  # Поиск
    fieldsets = (
        (None, {
            'fields': ('user', 'email', 'name', 'comment')
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject_letter', 'user')
    list_filter = ('user',)
    search_fields = ('subject_letter',)
    fieldsets = (
        (None, {
            'fields': ('user', 'subject_letter', 'body_letter')
        }),
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'status', 'first_send_datetime', 'end_send_datetime', 'user',)
    list_filter = ('status', 'user',)
    search_fields = ('message__subject_letter',)
    filter_horizontal = ('recipient',)
    fieldsets = (
        (None, {
            'fields': ('user', 'message', 'recipient', 'status', 'first_send_datetime', 'end_send_datetime')
        }),
    )


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_datetime', 'status', 'user')
    list_filter = ('status', 'mailing__user')
    readonly_fields = ('mail_server_response',)  # Делаем поле только для чтения
    fieldsets = (
        (None, {
            'fields': ('mailing', 'attempt_datetime', 'status', 'mail_server_response', 'user')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(mailing__user=request.user)
        return qs
