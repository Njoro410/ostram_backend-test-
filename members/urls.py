from django.urls import path
from .views import MemberList, MemberDetail, ResidentialAreaList, ResidentialAreaDetail

urlpatterns = [
  path('members/view/', MemberList.as_view()),
  path('members/create/', MemberList.as_view()),
  path('members/<int:pk>/', MemberDetail.as_view()),
  path('residential-areas/view/', ResidentialAreaList.as_view()),
  path('residential-areas/create/', ResidentialAreaList.as_view()),
  path('residential-areas/<int:pk>/', ResidentialAreaDetail.as_view()),
]