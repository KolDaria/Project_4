from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from mailing.models import Mailing
from mailing.services import send_mailing


class Command(BaseCommand):
    help = "Запускает или завершает рассылку"

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']

        try:
            mailing = Mailing.objects.get(pk=mailing_id)

            if mailing.status == 'created' or mailing.status == 'completed':
                send_mailing(mailing)
                mailing.status = 'running'
                if mailing.first_send_datetime is None:
                    mailing.first_send_datetime = timezone.now()
                mailing.end_send_datetime = timezone.now()
                with transaction.atomic():
                    mailing.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Рассылка '{mailing.message.subject_letter}' (ID: {mailing_id}) запущена."))

            elif mailing.status == 'running':
                mailing.status = 'completed'
                mailing.end_send_datetime = timezone.now()
                mailing.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Рассылка '{mailing.message.subject_letter}' (ID: {mailing_id}) завершена."))
            else:
                 self.stdout.write(self.style.WARNING(f"Рассылка '{mailing.message.subject_letter}' "
                                                      f"(ID: {mailing_id}) не может быть запущена или завершена."))

        except Mailing.DoesNotExist:
            raise CommandError(f'Рассылка с ID {mailing_id} не найдена.')
        except Exception as e:
            raise CommandError(f'Ошибка: {e}')
