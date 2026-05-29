from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Division

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra', {'fields': ('full_name', 'division', 'avatar', 'role', 'last_ip', 'last_seen')}),
    )

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
