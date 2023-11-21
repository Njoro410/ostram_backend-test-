import requests
from django.http import JsonResponse
from .helper import format_phone_number
from loans.models import Loans

# Function to create the common payload


def global_payload(mobile, msg):
    return {
        "userid": "njoro410",
        "password": "j47xfDkE",
        "mobile": format_phone_number(mobile),
        "msg": msg,
        "senderid": "OstramSacco",
        "msgType": "text",
        "duplicatecheck": "true",
        "output": "json",
        "sendMethod": "quick",
    }


def send_sms(payload):
    url = "https://smsportal.hostpinnacle.co.ke/SMSApi/send"
    headers = {
        "apikey": "dfa53a442d5248555b977a97ad1172d4276eaf5b",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return True
    except Exception as e:
        print(e)

    return False

# Function to send SMS to a single recipient
def send_one_sms(recipient_number, revised_message):
    payload = global_payload(recipient_number, revised_message)

    if send_sms(payload):
        return True

    return False


# Function to send SMS to multiple recipients
def send_bulk_sms(recipient_number, revised_message):
    payload = global_payload(recipient_number, revised_message)

    if send_sms(payload):
        return True

    return False


# Function to send SMS to all members
def send_broadcast_sms(recipient_number, revised_message):
    payload = global_payload(recipient_number, revised_message)

    if send_sms(payload):
        print(recipient_number, revised_message)
        return True

    return False

# Function to send welcome SMS to a new member
def send_welcome_sms(recipient_number, recipient_name):
    message_body = f"Dear {recipient_name}, Welcome to our Sacco family! We are thrilled to have you on board and we sincerely appreciate your decision to join us."
    payload = global_payload(recipient_number, message_body)

    if send_sms(payload):
        return True

    return False

# Function to send loan status to members


def send_loan_status_sms(loan_id, status_name):
    loan = Loans.objects.get(id=loan_id)
    try:
        if status_name == "APPROVED":
            message_body = f"Dear {loan.member.names}, your loan application has been approved. Please check your email for more details."
            recipient_number = loan.member.phone_no
            payload = global_payload(recipient_number, message_body)

            if send_sms(payload):
                print(message_body)
                return True

        elif status_name == "DENIED":
            message_body = f"Dear {loan.member.names}, your loan application has been rejected. Please check your email for more details."
            recipient_number = loan.member.phone_no
            payload = global_payload(recipient_number, message_body)

            if send_sms(payload):
                print(message_body)
                return True
        elif status_name == "DISBURSED":
            message_body = f"Dear {loan.member.names}, your loan has been disbursed. Please check your email for more details."
            recipient_number = loan.member.phone_no
            payload = global_payload(recipient_number, message_body)

            if send_sms(payload):
                print("message disbursed sent")
                return True
            
        elif status_name == "CANCELLED":
            message_body = f"Dear {loan.member.names}, your loan has been cancelled. Please check your email for more details."
            recipient_number = loan.member.phone_no
            payload = global_payload(recipient_number, message_body)

            if send_sms(payload):
                print(message_body)
                return True
            
        elif status_name == "CLOSED":
            message_body = f"Dear {loan.member.names}, your loan has been closed. Thank you for trusting in us."
            recipient_number = loan.member.phone_no
            payload = global_payload(recipient_number, message_body)

            if send_sms(payload):
                print(message_body)
                return True

    except Exception as e:
        # print(e)
        return False


def send_guarantors_text(loan_id,guarantor_id):
    print(loan_id,guarantor_id)