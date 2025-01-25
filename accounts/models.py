from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from datetime import date


class User(AbstractUser):
    """
    Mainain some basic information about members for logistics/coordinating
    purposes

    * User name, email, password are built into the allauth model
    """
    first_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=_("first name")
    )
    last_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=_("last name")
    )
    phone_number = models.CharField(
        blank=True, null=True, verbose_name=_("phone number")
    )
    postal_code = models.CharField(
        blank=True, null=True, verbose_name=_("postal code")
    )
    # for keeping track of how many people each member order feeds
    members_per_account = models.IntegerField(
        default=1, verbose_name=_("members per account")
    )

    def __str__(self):
        return self.username  # or any other string representation you prefer


class GroupMembership(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("user")
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, verbose_name=_("group")
    )
    expiration_date = models.DateField(
        blank=True, null=True, verbose_name=_("expiration date")
    )

    class Meta:
        verbose_name = _("group membership")

    def is_active(self):
        return self.expiration_date >= date.today()
