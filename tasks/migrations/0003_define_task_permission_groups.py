from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from tasks.constants import TASKS


def create_group_permissions(apps, schema_editor):
    # Loop through the TASKS dictionary to create groups and assign permissions
    for task_name, task_info in TASKS.items():
        if task_info['db_object']:
            for obj in task_info['db_object']:
                group_name = task_info['description']
                group, created = Group.objects.get_or_create(name=group_name)

                # Assign existing permissions to the group
                content = ContentType.objects.get_for_model(obj)
                permissions = Permission.objects.filter(content_type=content)
                for permission in permissions:
                    group.permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_seed_tasks'),
        ('baskets', '0002_seed_baskets'),
        ('products', '0002_import_products'),
    ]

    operations = [
        migrations.RunPython(create_group_permissions),
    ]
