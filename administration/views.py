from django.shortcuts import render
from .models import Branch,BranchStatus
from .serializers import BranchSerializer,BranchStatusSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


def create_branch(request):
    pass


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def manage_branches(request, id=None):
    if request.method == 'GET':
        # if no branch id, return all branches
        if id is None:
            branches = Branch.objects.all()
            if not branches:
                return Response({'message': 'No branches available'}, status=status.HTTP_404_NOT_FOUND)
            serializer = BranchSerializer(branches, many=True)
            return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                branch = Branch.objects.get(id=id)
            except Branch.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BranchSerializer(branch)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Branch created successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Branch creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            branch = Branch.objects.get(id=id)
        except Branch.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BranchSerializer(branch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Branch updated successfully", "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Branch update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            branch = Branch.objects.get(id=id)
        except Branch.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        branch.delete()
        return Response({"message": "Branch deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
# a function got getting and creating loan status
def branch_status(request):
    if request.method == 'GET':
        try:
            branch_status = BranchStatus.objects.all()
        except BranchStatus.DoesNotExist():
            return Response({'message': 'Branch status not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BranchStatusSerializer(branch_status, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = BranchStatusSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Branch status created successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Branch status creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
