from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Define your groups and permissions here
        groups_permissions = {
            'Restaurant': [
                'add_products', 
                'change_products', 
                'delete_products', 
                'view_products'
            ],
            'Waiter': ['add_products', 'change_products'],
            'Client': ['view_products'],
        }

        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Group "{group_name}" created')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Group "{group_name}" already exists')
                )

            # Assign permissions to group
            for codename in permissions:
                try:
                    permission = Permission.objects.get(
                        content_type__app_label='restaurants',
                        codename=codename
                    )
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission "{codename}" not found'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions have been set up'))
