from django.core.management.base import BaseCommand
from django.utils import timezone

from mailing.models import Mailing


class Command(BaseCommand):
    help = "Запускает или завершает рассылку"

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')
        parser.add_argument('action', type=str, choices=['start', 'complete'], help='Действие: start или complete')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        action = options['action']

        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка с ID {mailing_id} не найдена'))
            return

        if action == 'start':
            mailing.first_send_datetime = timezone.now()
        elif action == 'complete':
            mailing.end_send_datetime = timezone.now()

        mailing.update_status()
        mailing.save()

        self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing.pk} ({action})'))
