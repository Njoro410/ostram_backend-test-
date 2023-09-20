from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginView),
    path('register/', views.registerView),
    path('refresh-token/', views.CookieTokenRefreshView.as_view()),
    path('logout', views.logoutView),
    path('user',views.userDetails),
    path('permissions/', views.permission_list, name='permissions-list'),
    path('all-users/', views.all_users, name='users-without-id'),
    path('user_id/<int:user_id>/', views.all_users, name='users-with-id'),
    path('all_permission_groups/', views.all_permission_groups, name='all_permission_groups'),
    path('delete_permission_group/', views.delete_permission_group, name='delete_permission_group'),
]
