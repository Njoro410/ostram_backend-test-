from django.shortcuts import render
from rest_framework.decorators import api_view
import requests
from rest_framework.response import Response
from rest_framework import status
from members.models import Members
from sms.utils import send_one_sms,send_bulk_sms,send_broadcast_sms
from sms.helper import sentence_case

# Create your views here.


@api_view(['POST'])
def send_single_sms(request):
    message = request.data.get('message')
    member_no = request.data.get('member')

    try:
        member = Members.objects.get(mbr_no=member_no)
    except Members.DoesNotExist:
        return Response({'message': 'Member does not exist'}, status=status.HTTP_404_NOT_FOUND)

    recipient_number = member.phone_no
    revised_message = f"Dear {sentence_case(member.names)}, {message}"
    if send_one_sms(recipient_number, revised_message):
        return Response({"message": f"SMS sent to {sentence_case(member.names)} successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "SMS not sent"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_multiple_sms(request):
    message = request.data.get('message')
    members = request.data.get('members')
    
    success_responses = []
    failure_responses = []

    for member_id in members:
        try:
            member = Members.objects.get(mbr_no=member_id)
            recipient_number = member.phone_no
            revised_message = f"Dear {sentence_case(member.names)}, {message}"

            if send_bulk_sms(recipient_number, revised_message):
                success_responses.append(f"SMS sent to {sentence_case(member.names)} successfully>>")
            else:
                failure_responses.append(f"Failed to send SMS to {sentence_case(member.names)}>>")
        except Members.DoesNotExist:
            failure_responses.append(f"Member with ID {member_id} not found")

    if success_responses:
        return Response({"message": success_responses}, status=status.HTTP_200_OK)
    else:
        return Response({"message": failure_responses}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
def broadcast_sms(request):
    message = request.data.get('message')

    members = Members.objects.all()
    
    success_responses = []
    failure_responses = []

    for member in members:
        try:
            recipient_number = member.phone_no
            revised_message = f"Dear {sentence_case(member.names)}, {message}"

            if send_broadcast_sms(recipient_number, revised_message):
                success_responses.append(f"SMS sent to {sentence_case(member.names)} successfully")
            else:
                failure_responses.append(f"Failed to send SMS to {sentence_case(member.names)}")
        except Exception as e:
            failure_responses.append(f"Failed to send SMS to member ID {member.mbr_no}: {str(e)}")

    if success_responses:
        return Response({"message": success_responses}, status=status.HTTP_200_OK)
    else:
        return Response({"message": failure_responses}, status=status.HTTP_400_BAD_REQUEST)
