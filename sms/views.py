from django.shortcuts import render
from rest_framework.decorators import api_view
import requests
from rest_framework.response import Response
from rest_framework import status
from members.models import Members
from sms.utils import send_one_sms, send_bulk_sms, send_broadcast_sms
from sms.helper import sentence_case_first_name

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
    revised_message = f"Dear {sentence_case_first_name(member.names)}, {message}"
    if send_one_sms(recipient_number, revised_message):
        return Response({"message": f"SMS sent to {sentence_case_first_name(member.names)} successfully"}, status=status.HTTP_200_OK)
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
            revised_message = f"Dear {sentence_case_first_name(member.names)}, {message}"

            if send_bulk_sms(recipient_number, revised_message):
                success_responses.append(
                    f"SMS sent to {sentence_case_first_name(member.names)} successfully>>")
            else:
                failure_responses.append(
                    f"Failed to send SMS to {sentence_case_first_name(member.names)}>>")
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
            revised_message = f"Dear {sentence_case_first_name(member.names)}, {message}"

            if send_broadcast_sms(recipient_number, revised_message):
                success_responses.append(f"SMS sent to {sentence_case_first_name(member.names)} successfully")
            else:
                failure_responses.append(f"Failed to send SMS to {sentence_case_first_name(member.names)}")
        except Exception as e:
            failure_responses.append(f"Failed to send SMS to member ID {member.mbr_no}: {str(e)}")

    if success_responses:
        return Response({"message": success_responses}, status=status.HTTP_200_OK)
    else:
        return Response({"message": failure_responses}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def broadcast_sms(request):
#     try:
#         message = request.data.get('message')
#         members = Members.objects.all()
#         success_responses, failure_responses = process_members(
#             members, message)

#         if success_responses:
#             return Response({"message": success_responses}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": failure_responses}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def process_members(members, message):
#     success_responses = []
#     failure_responses = []

#     for member in members:
#         try:
#             process_member(member, message, success_responses,
#                            failure_responses)
#         except Exception as e:
#             failure_responses.append(
#                 f"Failed to send SMS to member ID {member.mbr_no}: {str(e)}")

#     return success_responses, failure_responses


# def process_member(member, message, success_responses, failure_responses):
#     recipient_number = member.phone_no
#     prefix = recipient_number[:4]
#     # Define the allowed prefixes
#     allowed_prefixes = [
#         "0701", "0702", "0703", "0704", "0705", "0706", "0707", "0708",
#         "0710", "0711", "0712", "0713", "0714", "0715", "0716", "0717",
#         "0718", "0719", "0720", "0721", "0722", "0723", "0724", "0725",
#         "0726", "0727", "0728", "0729", "0740", "0741", "0742", "0743", "0746",
#         "0748", "0790", "0791", "0792", "0793", "0794", "0795", "0796",
#         "0797", "0798", "0799", '0110', '0111', '0112', '0113', '0114', '0115'
#     ]

#     if prefix in allowed_prefixes:
#         revised_message = f"Dear {sentence_case_first_name(member.names)}, {message}"

#         if send_broadcast_sms(recipient_number, revised_message):
#             success_responses.append(
#                 f"SMS sent to {sentence_case_first_name(member.names)} successfully")
#         else:
#             failure_responses.append(
#                 f"Failed to send SMS to {sentence_case_first_name(member.names)}")
#     else:
#         failure_responses.append(
#             f"SMS not sent to {sentence_case_first_name(member.names)}: Invalid prefix")
