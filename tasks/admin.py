from django.contrib import admin
from .models import Task, PublishTask, AssignTask, TaskTimeSlot


class AssignTaskInline(admin.TabularInline):
    model = AssignTask
    extra = 1


class TaskTimeSlotInline(admin.TabularInline):
    model = TaskTimeSlot
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'operation_order', 'icon_svg_markup')
    search_fields = ('name', 'description')
    inlines = [TaskTimeSlotInline]


@admin.register(PublishTask)
class PublishTaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'task_description', 'published_at', 'valid_until')
    search_fields = ('task',)


@admin.register(AssignTask)
class AssignTaskAdmin(admin.ModelAdmin):
    list_display = ('task_and_time_slot', 'volunteer', 'assigned_at', 'expiration_date', 'user_notes')
    search_fields = ('volunteer',)


@admin.register(TaskTimeSlot)
class TaskTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('task', 'day_of_week', 'time_start', 'duration', 'min_req_volunteers')
    search_fields = ('task', 'day_of_week', 'time_start', 'duration')
