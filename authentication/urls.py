from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginView),
    path('register', views.registerView),
    path('refresh-token', views.CookieTokenRefreshView.as_view()),
    path('logout', views.logoutView),
    path('user',views.userDetails)
]
