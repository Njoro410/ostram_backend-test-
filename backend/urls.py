"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/loans/',include('loans.urls')),
    path('api/savings/',include('savings.urls')),
    path('api/deposits/',include('deposits.urls')),
    path('api/assets/',include('assetmanager.urls')),
    path('api/members/',include('members.urls')),
    path('api/auth/',include(('authentication.urls','authentication'), namespace="authentication")),
    path('api/stats/',include('stats.urls')),
    path('api/todos/',include('todo.urls')),
    path('api/transactions/',include('mpesa.urls')),
    path('api/contributions/', include('contributions.urls'))


]
