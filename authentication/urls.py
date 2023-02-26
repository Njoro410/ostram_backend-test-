from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginView),
    path('register', views.registerView),
    path('refresh-token', views.refreshTokenView),
    path('logout', views.logoutView),
]
