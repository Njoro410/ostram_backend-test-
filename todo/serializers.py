from .models import Todo
from rest_framework import serializers

class TodoSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField(read_only=True)
    assignee = serializers.SerializerMethodField(read_only=True)
    
    def get_creator(self, todo):
        if todo.created_by:
            creator = todo.created_by.fullname
            return creator
        return None  # Or any other default value you want to use when created_by is None

    
    def get_assignee(self, todo):
        if todo.created_by:
            assignee = todo.created_by.fullname
            return assignee
        return None
    
    class Meta:
        model = Todo
        fields = "__all__"