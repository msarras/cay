from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from .models import GroupMembership


class PermissionRequiredMixin(LoginRequiredMixin):
    group_name = None  # This will be set in the child class

    def dispatch(self, request, *args, **kwargs):
        if self.group_name is None:
            raise ValueError("You must set the 'group_name' attribute in the child class.")

        # Check if the user is logged in (handled by LoginRequiredMixin)
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        group = Group.objects.get(name=self.group_name)

        if not self.user_has_permission(request.user, group):
            return HttpResponseForbidden("You do not have permission to access this resource.")

        return super().dispatch(request, *args, **kwargs)

    def user_has_permission(self, user, group):
        """Check if the user has active membership in the specified group."""
        try:
            membership = GroupMembership.objects.get(
                    user=user, expiration_date__gte=date.today(), group=group)
            return membership.is_active()
        except GroupMembership.DoesNotExist:
            return False
