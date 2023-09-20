from django.urls import path
from . import views

urlpatterns = [
    path('get_user_todos/',views.todo_by_user_id,name='get_user_todos'),
    path('todo_by_id/<int:id>/',views.todo_by_id,name='todo_by_id'),
    path('create_todo/',views.create_todo,name='create_todo'),
    path('public_todos/',views.get_public_todos,name='public_todos'),
    path('user_assigned_todos/',views.user_assigned_todo,name='user_assigned_todo'),
    path('todo_status/',views.todo_status,name='todo_status'),
    path('todo_priority/',views.todo_priority,name='todo_priority'),
]
