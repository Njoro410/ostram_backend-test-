from django.urls import path
from .views import MemberList, MemberDetail, ResidentialAreaList, ResidentialAreaDetail

urlpatterns = [
  path('', MemberList.as_view()),
  path('member/<int:pk>/', MemberDetail.as_view()),
  path('residential-areas/', ResidentialAreaList.as_view()),
  path('residential-areas/<int:pk>/', ResidentialAreaDetail.as_view()),
]