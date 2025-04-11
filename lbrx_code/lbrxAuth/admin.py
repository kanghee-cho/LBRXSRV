from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LbrxUser

class LbrxUserAdmin(UserAdmin):
    list_display = ('email', 'nickname', 'is_active', 'is_staff', 'mfa_enabled')
    list_filter = ('is_active', 'is_staff', 'mfa_enabled')
    search_fields = ('email', 'nickname')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mfa_enabled', 'mfa_secret')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('mfa_enabled', 'mfa_secret')}),
    )

    admin.site.register(LbrxUser, LbrxUserAdmin)