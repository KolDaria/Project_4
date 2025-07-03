from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingAttempt


def send_mailing(mailing):
    for recipient in mailing.recipient.all():
        try:
            send_mail(
                subject=mailing.message.subject_letter,
                message=mailing.message.body_letter,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(mailing=mailing, status=True, server_response='OK')
        except Exception as e:
            MailingAttempt.objects.create(mailing=mailing, status=False, server_response=str(e))
