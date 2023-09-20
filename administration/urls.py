from django.urls import path
from . import views

urlpatterns = [
    path('all_branches/', views.manage_branches, name='all_branches'),
    path('specific_branch/<int:id>/', views.manage_branches, name='specific_branch'),
    path('branch_status/', views.branch_status, name='branch_status'),
]
