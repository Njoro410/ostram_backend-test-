from django.contrib import admin
from .models import staffAccount

@admin.register(staffAccount)
class CustomUserAdmin(admin.ModelAdmin):
    pass