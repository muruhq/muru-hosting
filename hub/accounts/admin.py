"""Accounts in the Django admin site, which local sign-in turns on."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from hub.accounts.models import User

admin.site.register(User, UserAdmin)
