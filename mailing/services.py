import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from mailing.models import MailingAttempt

logger = logging.getLogger(__name__)


def send_mailing(mailing):
    logger.debug(f"send_mailing запущена для рассылки {mailing.pk}. Mailing object: {mailing}")
    subject = mailing.message.subject_letter
    body = mailing.message.body_letter
    recipients = mailing.recipient.all()
    logger.debug(f"Получатели: {recipients}")

    for recipient in recipients:
        logger.debug(f"Отправка письма на {recipient.email}")
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [recipient.email],
                fail_silently=False,
            )
            status = 'successfully'
            response = 'Сообщение успешно отправлено'
            logger.debug(f"Успешно отправлено на {recipient.email}")

        except Exception as e:
            status = 'not successfully'
            response = str(e)
            logger.exception(f"Ошибка при отправке письма на {recipient.email}: {e}")

        logger.debug(f"Собираемся создать MailingAttempt. Данные: mailing={mailing}, status={status}, response={response}, user={mailing.user}")  # Перед созданием

        try:
            with transaction.atomic():  # Добавляем явную транзакцию
                attempt = MailingAttempt.objects.create(
                    mailing=mailing,
                    status=status,
                    mail_server_response=response,
                    user=mailing.user
                )
                logger.debug(
                    f"MailingAttempt успешно создан для {recipient.email}. Mailing ID: {mailing.pk}, Status: {status}, Attempt ID: {attempt.id}")  # Добавляем ID попытки
        except Exception as e:
            logger.error(f"Ошибка при создании MailingAttempt: {e}")
