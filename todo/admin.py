from django.contrib import admin
from .models import Todo, Priority, Status
from django import forms

# Register your models here.
admin.site.register(Priority)
admin.site.register(Status)


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'
        widgets = {
            'assigned_to': forms.CheckboxSelectMultiple
        }


class TodoAdmin(admin.ModelAdmin):
    form = TodoForm


admin.site.register(Todo, TodoAdmin)
