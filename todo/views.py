from django.shortcuts import render
from .models import Todo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from members.models import Members
from django.shortcuts import get_object_or_404
from datetime import date
from .serializers import TodoSerializer, StatusSerializer, PrioritySerializer
from .models import Todo, Status, Priority
# Create your views here.


@api_view(['POST'])
def create_todo(request):
    serializer = TodoSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Todo created successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Todo creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def todo_by_user_id(request):
    try:
        todos = Todo.objects.filter(created_by_id=request.user.id)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todos, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def user_assigned_todo(request):
    try:
        todos = Todo.objects.filter(assigned_to=request.user.id)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todos, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
def todo_by_id(request, id):
    try:
        todo = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Todo updated successfully", "results": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Todo update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response({"message": "Todo deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_public_todos(request):
    try:
        todos = Todo.objects.filter(public=True)
    except Todo.DoesNotExist:
        return Response({'message': 'No todos to display'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todos, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def todo_status(request):
    if request.method == 'GET':
        try:
            todo_status = Status.objects.all()
        except Status.DoesNotExist():
            return Response({'Error': 'Task status not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StatusSerializer(todo_status, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = StatusSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Task status created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Task status creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
@api_view(['GET', 'POST'])
def todo_priority(request):
    if request.method == 'GET':
        try:
            todo_priority = Priority.objects.all()
        except Priority.DoesNotExist():
            return Response({'Error': 'Task priority not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PrioritySerializer(todo_priority, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = PrioritySerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Task priority created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Task priority creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
