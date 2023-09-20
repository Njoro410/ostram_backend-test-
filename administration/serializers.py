from .models import Branch, BranchStatus
from rest_framework import serializers
from authentication.models import staffAccount


class StaffAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = staffAccount
        fields = ['first_name','last_name','phone_number','email','is_active','is_admin']


class BranchSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    branch_status_name = serializers.SerializerMethodField(read_only=True)
    creator = serializers.SerializerMethodField(read_only=True)
    staff = serializers.SerializerMethodField(read_only=True)

    def get_manager_name(self, branch):
        if branch.manager:
            manager_name = f'{branch.manager.first_name} {branch.manager.last_name}'
            return manager_name
        return None

    def get_name(self, branch):
        if branch.location:
            location_name = branch.location.name
            return location_name
        return None

    def get_branch_status_name(self, branch):
        if branch.status:
            status_name = branch.status.name
            return status_name
        return None

    def get_creator(self, branch):
        if branch.created_by:
            creator = f'{branch.created_by.first_name} {branch.created_by.last_name}'
            return creator
        return None

    def get_staff(self, branch):
        staff_members = staffAccount.objects.filter(branch=branch)
        staff_serializer = StaffAccountSerializer(staff_members, many=True)
        return staff_serializer.data

    class Meta:
        model = Branch
        fields = "__all__"



class BranchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchStatus
        fields = "__all__"