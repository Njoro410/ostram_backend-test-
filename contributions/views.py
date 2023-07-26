from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import DailyContributionsSerializer
from rest_framework import status
from .models import DailyContributions

# Create your views here.
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def daily_contributions(request):
    if request.method == 'GET':
        try:
            all_contributions = DailyContributions.objects.all()
        except DailyContributions.DoesNotExist:
            return Response({"error": "There are no daily contributions"},status=status.HTTP_404_NOT_FOUND)
        serializer = DailyContributionsSerializer(all_contributions, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = DailyContributionsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contribution saved successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
        # code to distribute values to different accounts
        else:
            return Response({"message": "Contribution posting failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
