from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import DailyContributionsSerializer
from rest_framework import status
from .models import DailyContributions
import datetime
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def daily_contributions(request):

    if request.method == 'GET':
        year = request.query_params.get('year', datetime.datetime.now().year)
        month = request.query_params.get('month', None)
        quarter = request.query_params.get('quarter', None)

        try:
            all_contributions = DailyContributions.objects.all()

            # Filter by year
            all_contributions = all_contributions.filter(received_date__year=year)

            # Filter by month
            if month:
                all_contributions = all_contributions.filter(received_date__month=month)

            # Filter by quarter (assuming quarter is represented as 1, 2, 3, or 4)
            if quarter:
                try:
                    quarter_num = int(quarter)
                    if 1 <= quarter_num <= 4:
                        quarter_months = [3 * quarter_num - 2, 3 * quarter_num - 1, 3 * quarter_num]
                        all_contributions = all_contributions.filter(received_date__month__in=quarter_months)
                    else:
                        return Response({"error": "Invalid quarter. Quarter must be between 1 and 4."}, status=status.HTTP_400_BAD_REQUEST)
                except ValueError:
                    return Response({"error": "Invalid quarter. Quarter must be an integer between 1 and 4."}, status=status.HTTP_400_BAD_REQUEST)

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
