from collections import defaultdict
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from datetime import date
from .models import AssignTask, Task, TaskTimeSlot, GroupMembership
from .utils import get_end_of_week


class TaskView(LoginRequiredMixin, View):
    template_name_task_selection = 'task_selection.html'
    template_name_assigned_tasks = 'assigned_tasks.html'

    now = date.today()

    def get(self, request, *args, **kwargs):
        user_tasks = AssignTask.objects.filter(
            expiration_date__gte=self.now,
            volunteer=request.user
        ).order_by('task_and_time_slot')

        if user_tasks.exists():
            # Get the task_and_time_slot of the user's tasks
            task_and_time_slots = user_tasks.values_list('task_and_time_slot', flat=True)

            # Find colleagues who have the same task_and_time_slot but
            # different volunteer
            colleagues = AssignTask.objects.filter(
                Q(task_and_time_slot__in=task_and_time_slots) &
                ~Q(volunteer=request.user)
            )
            # Create a dictionary to hold task names and associated volunteers
            task_volunteers = defaultdict(list)

            # Iterate through the colleagues queryset
            for colleague in colleagues:
                task_name = colleague.task_and_time_slot.task.name
                volunteer_username = colleague.volunteer.username
                task_volunteers[task_name].append(volunteer_username)

            # Convert lists of usernames to comma-separated strings
            task_volunteers = {task: ', '.join(volunteers) for task, volunteers in task_volunteers.items()}

            context = {
                'assigned_tasks': user_tasks,
                'others_assigned_to_task': task_volunteers,
            }
            return render(request, self.template_name_assigned_tasks, context)

        tasks = Task.objects.prefetch_related('time_slots')\
            .order_by('operation_order').all()
        assigned_time_slots = get_assigned_time_slots()

        context = {
            'tasks': tasks,
            'assigned_time_slots': assigned_time_slots,
        }
        return render(request, self.template_name_task_selection, context)

    def post(self, request, *args, **kwargs):
        if AssignTask.objects.filter(
                expiration_date__gte=self.now,
                volunteer=request.user).exists():
            return redirect('tasks:already_assigned')

        selected_time_slot_ids = request.POST.getlist('time_slots')
        for time_slot_id in selected_time_slot_ids:
            time_slot = get_object_or_404(TaskTimeSlot, id=time_slot_id)
            AssignTask.objects.create(
                    task_and_time_slot=time_slot,
                    expiration_date=get_end_of_week(),
                    volunteer=request.user)
            manage_group_membership(request.user, time_slot)

        return redirect('tasks:task_assigned')


class ModifyTaskAssignmentView(LoginRequiredMixin, View):
    template_name = 'task_selection.html'

    now = date.today()

    def get(self, request):
        tasks = Task.objects.prefetch_related('time_slots').order_by('operation_order').all()
        assigned_time_slots = get_assigned_time_slots()
        existing_assigned_task_ids = set(AssignTask.objects.filter(expiration_date__gte=self.now, volunteer=request.user).values_list('task_and_time_slot_id', flat=True))

        context = {
            'tasks': tasks,
            'assigned_time_slots': assigned_time_slots,
            'existing_assigned_time_slots': existing_assigned_task_ids,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        selected_time_slot_ids = request.POST.getlist('time_slots')
        user_tasks = AssignTask.objects.filter(
                expiration_date__gte=self.now,
                volunteer=request.user)

        # Delete unselected assignments
        user_tasks.exclude(task_and_time_slot__id__in=selected_time_slot_ids).delete()

        # Create or update assignments
        new_perms_groups = set()
        for time_slot_id in selected_time_slot_ids:
            time_slot = get_object_or_404(TaskTimeSlot, id=time_slot_id)
            AssignTask.objects.get_or_create(task_and_time_slot=time_slot, volunteer=request.user, expiration_date=get_end_of_week())
            new_perms_groups.add(time_slot.task.description)
            manage_group_membership(request.user, time_slot)

        # Clean up old memberships
        GroupMembership.objects.filter(user=request.user).exclude(group__name__in=new_perms_groups).delete()

        return redirect('tasks:task_assigned')


class CancelTaskAssignmentView(LoginRequiredMixin, View):
    def post(self, request):
        # Get all assignments for the logged-in user
        assignments = AssignTask.objects.filter(volunteer=request.user)
        permissions = GroupMembership.objects.filter(user=request.user)

        # Delete the assignments if they exist
        for user_property in [assignments, permissions]:
            if user_property.exists():
                user_property.delete()

        return redirect('tasks:list')


@login_required
def task_assigned(request):
    return render(request, 'received_task_assignment_request.html')


def get_assigned_time_slots():
    assigned_tasks = AssignTask.objects.select_related('volunteer')\
        .filter(expiration_date__gte=date.today())\
        .values('task_and_time_slot', 'task_and_time_slot__task__name', 'volunteer__username')

    assigned_time_slots = {}
    for task in assigned_tasks:
        time_slot_id = task['task_and_time_slot']
        username = task['volunteer__username']
        assigned_time_slots.setdefault(time_slot_id, []).append(username)

    return assigned_time_slots


def manage_group_membership(user, time_slot):
    perms = Group.objects.filter(name=time_slot.task.description).first()
    if perms:
        perms.user_set.add(user)
        GroupMembership.objects.update_or_create(
            user=user,
            group=perms,
            expiration_date=get_end_of_week()
        )
