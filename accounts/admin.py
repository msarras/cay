# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, GroupMembership


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'phone_number', 'postal_code', 'members_per_account',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'expiration_date')
    search_fields = ('user', 'group', 'expiration_date')
