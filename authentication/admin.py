from django.contrib import admin
from .models import staffAccount


@admin.register(staffAccount)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    filter_horizontal = ('groups', 'user_permissions',)

    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super().get_fieldsets(request, obj)
    #     fieldsets += (
    #         ('Personal Information', {
    #             'fields': ('username', 'email', 'first_name', 'last_name', 'title', 'role', 'phone_number', 'gender', 'dob', 'current_salary', 'reports_to')
    #         }),
    #         ('Groups and Permissions', {
    #             'fields': ('is_staff', 'is_admin', 'is_superuser', 'is_active', 'groups', 'user_permissions'),
    #         }),
    #     )
    #     return fieldsets
