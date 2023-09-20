from django.db import models
from django.conf import settings

# Create your models here.

class Priority(models.Model):
    name = models.CharField(max_length=50)
    # created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='todo_instance_creator', blank=True, null=True)
    # updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    # updated_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='todo_instance_updater', null=True)

    def __str__(self):
        return self.name
    
class Status(models.Model):
    name = models.CharField(max_length=50)
    # created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='todo_instance_creator', blank=True, null=True)
    # updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    # updated_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='todo_instance_updater', null=True)
    
    def __str__(self):
        return self.name
    

class Todo(models.Model):
    title = models.CharField(max_length=50, null=True)
    description = models.TextField()
    public = models.BooleanField(default=False)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    due_date = models.DateField()
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  related_name='todo_assigned')
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='todo_instance_creator', blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name='todo_instance_updater', null=True)
    
    def __str__(self):
        return self.title
    

    