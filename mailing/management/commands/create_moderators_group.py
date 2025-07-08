from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает группу модераторов с необходимыми правами'

    def handle(self, *args, **options):
        group_name = 'Модераторы'
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            permissions_data = [
                {
                    'app_label': 'mailing',
                    'model': 'mailing',
                    'codename': 'can_set_mailing_status',
                },
                {
                    'app_label': 'mailing',
                    'model': 'mailing',
                    'codename': 'can_disable_mailing',
                },
                {
                    'app_label': 'mailing',
                    'model': 'mailing',
                    'codename': 'can_complete_mailing',
                },
                {
                    'app_label': 'mailing',
                    'model': 'mailing',
                    'codename': 'can_view_all_mailings',
                },
                {
                    'app_label': 'users',
                    'model': 'user',
                    'codename': 'can_block_user',
                },
                {
                    'app_label': 'users',
                    'model': 'user',
                    'codename': 'can_view_user',
                },
            ]
        for perm_data in permissions_data:
            try:
                # Получаем content type
                content_type = ContentType.objects.get(app_label=perm_data['app_label'], model=perm_data['model'])
                # Получаем или создаем разрешение
                permission, created = Permission.objects.get_or_create(
                    codename=perm_data['codename'],
                    content_type=content_type,
                    name=f"Can {perm_data['codename'].replace('can_', '').replace('_', ' ')}"
                    # Пример формирования имени права
                )
                group.permissions.add(permission)
                self.stdout.write(
                    self.style.SUCCESS(f"Право '{perm_data['codename']}' добавлено в группу '{group_name}'"))
            except ContentType.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"ContentType для app_label='{perm_data['app_label']}' и model='{perm_data['model']}' не найден."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при добавлении права '{perm_data['codename']}': {e}"))

            group.save()
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_name}' успешно создана и права добавлены."))

        else:
            self.stdout.write(self.style.WARNING(f"Группа '{group_name}' уже существует."))
