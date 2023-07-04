from django.urls import path
from . import views

urlpatterns = [
    path('get_user_todos/<int:user_id>/',views.todo_by_user_id,name='get_user_todos'),
    path('todo_by_id/<int:id>/',views.todo_by_id,name='todo_by_id'),
    path('create_todo/',views.create_todo,name='create_todo'),
    path('public_todos/',views.get_public_todos,name='public_todos')
]
