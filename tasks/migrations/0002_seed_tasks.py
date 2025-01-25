from django.db import migrations

from tasks.constants import TASKS


def create_initial_tasks(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    TaskTimeSlot = apps.get_model('tasks', 'TaskTimeSlot')

    for task_name, task_info in TASKS.items():
        # Create the Task instance
        task, created = Task.objects.get_or_create(
            name=task_name,
            description=task_info.get('description'),
            operation_order=task_info.get('operation_order'),
            icon_svg_markup=task_info.get('icon_svg_markup')
        )

        # Create TaskTimeSlot instances if time slots are defined
        for time_slot in task_info.get('time_slots', []):
            TaskTimeSlot.objects.get_or_create(
                task=task,
                day_of_week=time_slot['day_of_week'],
                time_start=time_slot['time_start'],
                duration=time_slot['duration'],
                min_req_volunteers=time_slot['min_req_volunteers'],
            )


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_tasks),
    ]
