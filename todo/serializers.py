from .models import Todo, Status, Priority
from rest_framework import serializers
from authentication.models import staffAccount
 
class TodoSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(many=True, queryset=staffAccount.objects.all(), required=False)
    creator = serializers.SerializerMethodField(read_only=True)
    creator_email = serializers.SerializerMethodField(read_only=True)
    assignees = serializers.SerializerMethodField(read_only=True)
    priority_name = serializers.SerializerMethodField(read_only=True)
    status_name = serializers.SerializerMethodField(read_only=True)
    
    
    def save(self, **kwargs):
        user = self.context['request'].user
        kwargs['created_by'] = user
        return super().save(**kwargs)
    
    def get_creator(self, todo):
        if todo.created_by:
            creator = f'{todo.created_by.first_name} {todo.created_by.last_name}'
            return creator
        return None  
    
    def get_creator_email(self, todo):
        if todo.created_by:
            email = todo.created_by.email
            return email
        return None  
    
    def get_assignees(self, todo): 
        if todo.assigned_to:
            assignees = todo.assigned_to.all()
            assignees_list = []
            for assignee in assignees:
                assignees_data = {
                    'full_name': f'{assignee.first_name} {assignee.last_name}',
                }
                assignees_list.append(assignees_data)
            return assignees_list
        return None
    
    def get_priority_name(self, todo):
        if todo.priority:
            priority = todo.priority.name
            return priority
        return None
    
    def get_status_name(self, todo):
        if todo.status:
            status = todo.status.name
            return status
        return None
    
    class Meta:
        model = Todo
        fields = "__all__"
        

class StatusSerializer(serializers.ModelSerializer):
        
    def save(self, **kwargs):
        user = self.context['request'].user
        kwargs['created_by'] = user
        return super().save(**kwargs)
    
    class Meta:
        model = Status
        fields = "__all__"
        
class PrioritySerializer(serializers.ModelSerializer):
        
    def save(self, **kwargs):
        user = self.context['request'].user
        kwargs['created_by'] = user
        return super().save(**kwargs)
    
    class Meta:
        model = Priority
        fields = "__all__"