from django.conf import settings
from django.db import models


class Recipient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipients', default=1)
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Email",
        help_text="Введите email",
    )
    name = models.CharField(
        max_length=250,
        verbose_name="Ф.И.О",
        help_text="Укажите фамилию, имя, отчество",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        help_text="Напишите комментарий",
    )

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ['email', 'name']
        permissions = [
            ("can_view_recipient", "Может просматривать получателя"),
        ]


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages', default=1)
    subject_letter = models.CharField(
        max_length=200, verbose_name='Тема письма', help_text='Укажите тему письма',
    )
    body_letter = models.TextField(
        verbose_name="Тело письма",
        help_text="Укажите текст письма",
    )

    def __str__(self):
        return self.subject_letter

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['subject_letter']
        permissions = [
            ("can_view_message", "Можно просмотреть сообщение"),
        ]


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mailings', default=1)
    first_send_datetime = models.DateTimeField(
        verbose_name="Дата и время первой отправки",
        blank=True,
        null=True,
        help_text="Дата и время первой отправки (может быть пустым, если рассылка еще не запущена)",
    )

    end_send_datetime = models.DateTimeField(
        verbose_name="Дата и время окончания отправки",
        blank=True,
        null=True,
        help_text="Дата и время окончания отправки (может быть пустым, если рассылка еще не завершена)",
    )

    status = models.CharField(
        verbose_name="Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default='Создана',
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ManyToManyField(Recipient)

    def update_status(self):
        """Обновляет статус рассылки на основе дат отправки."""
        if self.end_send_datetime:
            self.status = 'completed'
        elif self.first_send_datetime:
            self.status = 'running'
        else:
            self.status = 'created'

    def save(self, *args, **kwargs):
        """Переопределяем метод save для автоматического обновления статуса."""
        self.update_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Рассылка {self.pk} - {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ['status']
        permissions = [
            ("can_set_mailing_status", "Можно установить статус рассылки"),
            ("can_disable_mailing", "Может отключать рассылку"),
            ("can_complete_mailing", "Может завершать рассылку"),
            ("can_view_all_mailings", "Может просмотреть все рассылки"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('successfully', 'Успешно'),
        ('not successfully', 'Не успешно'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    attempt_datetime = models.DateTimeField(
        verbose_name="Дата и время попытки",
        auto_now_add=True,
        help_text="Дата и время попытки",
    )

    status = models.CharField(
        verbose_name="Статус",
        max_length=20,
        choices=STATUS_CHOICES,
    )

    mail_server_response = models.TextField(
        verbose_name="Ответ почтового сервера",
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Попытка рассылки {self.mailing} - {self.attempt_datetime}"

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
