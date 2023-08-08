from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from rest_framework import status
from . import serializers, models
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import update_last_login
from rest_framework.parsers import JSONParser 
# Create your views here.


def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "accessToken": str(refresh.access_token),
        "refreshToken": str(refresh)
    }


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def loginView(request):
    serializer = serializers.loginSerializer(data=request.data)
    serializer.is_valid()

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = authenticate(email=email, password=password)

    if user is not None:
        update_last_login(None, user)
        tokens = get_user_tokens(user)
        res = response.Response()
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens["accessToken"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refreshToken"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.data = tokens
        res["X-CSRFToken"] = csrf.get_token(request)
        return res
    # raise rest_exceptions.AuthenticationFailed(
    #     "Email or Password is incorrect!", code=status.HTTP_400_BAD_REQUEST)
    return response.Response({"message": "Email or Password is incorrect!", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@rest_decorators.api_view(["POST", "PUT"])
@rest_decorators.permission_classes([])
def registerView(request):

    if request.method == 'POST':
        serializer = serializers.registrationSerializer(data=request.data)

        if serializer.is_valid():
            required_fields = ["username", "email", "reports_to",
                               "is_admin", "is_active", "is_staff", "is_superuser"]
            for field_name in required_fields:
                if field_name not in serializer.validated_data:
                    return response.Response({"message": "failed", "results": {field_name: ["This field may not be blank."]}}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()

            if user is not None:
                return response.Response({"message": "Staff registered successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)


@rest_decorators.api_view(['POST'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()

        res = response.Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"] = None

        return res
    except:
        raise rest_exceptions.ParseError("Invalid token")


class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')


class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)


@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def userDetails(request):
    if request.method == 'GET':
        try:
            user = models.staffAccount.objects.get(id=request.user.id)
        except models.staffAccount.DoesNotExist:
            return response.Response({"message": "User details not found"}, status=HTTP_404_NOT_FOUND)

        serializer = serializers.AccountSerializer(user)
        return response.Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)


@rest_decorators.api_view(["GET", "PUT"])
def all_users(request, user_id=None):
    if request.method == 'GET':
        if user_id is None:
            try:
                users = models.staffAccount.objects.all()
            except models.staffAccount.DoesNotExist:
                return response.Response({"message": "Users not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.AllAccountsSerializer(users, many=True)
            return response.Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                user = models.staffAccount.objects.get(id=user_id)
            except models.staffAccount.DoesNotExist:
                return response.Response({"message": "Users not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.AccountSerializer(user)
            return response.Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        user = models.staffAccount.objects.get(id=user_id)
        print(request.data)
        # data = JSONParser().parse(request)
        # print("user issss:",user)
        # print("data issss:",data)
        serializer = serializers.AccountSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response({"message": "Staff updated successfully", "results": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return response.Response({"message": "Staff updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return response.Response({"message": "failed", "results": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@rest_decorators.api_view(["GET"])
def permission_list(request):
    try:
        permissions = Permission.objects.all()
    except Permission.DoesNotExist:
        return response.Response({"message": "No permissions found"}, status=HTTP_404_NOT_FOUND)

    serializer = serializers.PermissionSerializer(permissions, many=True)
    return response.Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)


@rest_decorators.api_view(["GET", "POST"])
def all_permission_groups(request):
    try:
        groups = Group.objects.all()
    except Group.DoesNotExist:
        return response.Response({"message": "No permissions groups found"}, status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.GroupSerializer(groups, many=True)
        return response.Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = serializers.GroupSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({"message": "Permission group created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return response.Response({"message": "Permission group creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    






