from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from datetime import date

from accounts.models import User, GroupMembership


DAYS_OF_WEEK = [
    (0, _('Monday')),
    (1, _('Tuesday')),
    (2, _('Wednesday')),
    (3, _('Thursday')),
    (4, _('Friday')),
    (5, _('Saturday')),
    (6, _('Sunday')),
]


class Task(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_("name")
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    operation_order = models.IntegerField(
        blank=True, null=True, verbose_name=_("operation order")
    )
    icon_svg_markup = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("task")

    def __str__(self):
        return self.description

    def get_icon_url(self):
        """Return the full URL to the icon SVG file."""
        if self.icon_svg_file:
            return static(f'icons/{self.icon_svg_filename}')
        return None


class PublishTask(models.Model):
    task = models.ForeignKey(
        Task, related_name='publish_tasks', on_delete=models.CASCADE,
        verbose_name=_("task")
    )
    published_at = models.DateField(
        auto_now_add=True, null=True, verbose_name=_("published at")
    )
    valid_until = models.DateTimeField(
        blank=True, null=True, verbose_name=_("published at")
    )

    class Meta:
        verbose_name = _("publish task")

    def __str__(self):
        return f"{self.task} published on {self.published_at} valid until {self.valid_until}"

    def is_active(self):
        return self.valid_until >= date.today()

    @property
    def task_name(self):
        return self.task.name

    @property
    def task_description(self):
        return self.task.description


class TaskTimeSlot(models.Model):
    task = models.ForeignKey(
        Task, related_name='time_slots', verbose_name=_("task"),
        on_delete=models.CASCADE
    )
    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK, default=0, blank=True, null=True,
        verbose_name=_("jour de la semaine")
    )
    time_start = models.TimeField(
        blank=True, null=True, verbose_name=_("time start")
    )
    duration = models.DurationField(
        blank=True, null=True, verbose_name=_("duration")
    )
    min_req_volunteers = models.IntegerField(
        blank=True, null=True, verbose_name=_("minimum required volunteers")
    )

    class Meta:
        unique_together = ('task', 'day_of_week', 'time_start')
        verbose_name = _("task time slot")

    def save(self, *args, **kwargs):
        if self.duration.total_seconds() <= 0:
            raise ValueError("Duration must be greater than zero")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task} on {self.get_day_of_week_display()} from {self.time_start} for {self.duration}"

    @property
    def day_of_week_display(self):
        """Return the string representation of the day of the week."""
        return dict(DAYS_OF_WEEK).get(self.day_of_week, None)


class AssignTask(models.Model):
    task_and_time_slot = models.ForeignKey(
        TaskTimeSlot, on_delete=models.CASCADE,
        verbose_name=_("task time slot")
    )
    volunteer = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("volunteer")
    )
    assigned_at = models.DateField(
        auto_now_add=True, null=True, verbose_name=_("assigned at")
    )
    expiration_date = models.DateField(
        blank=True, null=True, verbose_name=_("expiration date")
    )
    user_notes = models.TextField(
        blank=True, null=True, verbose_name=_("comments")
    )

    class Meta:
        verbose_name = _("assign task")

    def __str__(self):
        return f"{self.task_and_time_slot} assigned to {self.volunteer.username}"

    def is_active(self):
        return self.expiration_date >= date.today()
