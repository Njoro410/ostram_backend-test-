from rest_framework import serializers
from django.conf import settings
from .models import staffAccount
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission,Group


class registrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})
    groups = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    permissions = serializers.ListField(
        child=serializers.CharField(), required=False
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password", "password2", "reports_to",
                  "is_admin", "is_active", "is_staff", "is_superuser", "groups", "permissions")

        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def save(self):
        email = self.validated_data.get("email")
        username = self.validated_data.get("username")
        reports_to = self.validated_data.get("reports_to")
        is_admin = self.validated_data.get("is_admin")
        is_active = self.validated_data.get("is_active")
        is_staff = self.validated_data.get("is_staff")
        is_superuser = self.validated_data.get("is_superuser")
        groups = self.validated_data.get("groups")
        permissions = self.validated_data.get("permissions")

        user = get_user_model()(
            email=email,
            username=username,
            reports_to=reports_to,
            is_admin=is_admin,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"})

        user.set_password(password)
        user.save()
        if groups is not None:
            user.groups.set(groups)

        if permissions is not None:
            user.user_permissions.set(permissions)
        return user


class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class AccountSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = get_user_model()
        fields = '__all__'
        
        
    def get_full_name(self, instance):
        if instance.first_name and instance.last_name:
            staff = f'{instance.first_name} {instance.last_name}'
            return staff
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        permissions = instance.user_permissions.all()
        representation['user_permissions'] = [
            {
                'id': permission.id,
                'name': permission.name, 
            }
            for permission in permissions
        ]

        groups = instance.groups.all()
        representation['groups'] = [
            {
                'id': group.id,
                'name': group.name,
                'permissions': [
                    {
                        'id': permission.id,
                        'name': permission.name,
                    }
                    for permission in group.permissions.all()
                ]
            }
            for group in groups
        ]

        reports_to_instance = instance.reports_to
        representation['reports_to'] = {
            'id': reports_to_instance.id,
            'name': f'{reports_to_instance.first_name} {reports_to_instance.last_name}',
        }

        return representation


class AllAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = staffAccount
        fields = ['id', 'email', 'username', 'first_name',
                  'last_name', 'is_admin', 'is_active']
        

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Combine the first and last name
        representation['full_name'] = f'{instance.first_name} {instance.last_name}'

        return representation
    
    
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'content_type', 'codename']
        

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)
    permission_list = serializers.SerializerMethodField()

    def get_permission_list(self, obj):
        permission_dict_list = []
        for permission in obj.permissions.all():
            permission_dict = {'id': permission.id, 'name': permission.name}
            permission_dict_list.append(permission_dict)
        return permission_dict_list

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'permission_list']

