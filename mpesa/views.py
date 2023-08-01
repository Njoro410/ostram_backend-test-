from django.shortcuts import render
import base64
import requests
import json
import os
from datetime import datetime
from .models import AccessToken, LipaNaMpesaCallback
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pytz


# Create your views here.


def get_access_token(request):
    consumer_key = 'tBY1Ym1xojZEyLUx0NApj9jHd0XmqhVF'
    consumer_secret = 'A9wV8AzEGMwD0RTx'
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    # Encode the consumer key and secret in base64
    api_key = base64.b64encode(
        f"{consumer_key}:{consumer_secret}".encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': f'Basic {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        access_token = response.json().get('access_token')

        # Retrieve the existing AccessToken object
        access_token_obj = AccessToken.objects.first()

        if access_token_obj:
            # Update the existing token
            access_token_obj.token = access_token
            access_token_obj.save()
        else:
            # If no existing token, create a new one
            AccessToken.objects.create(token=access_token)

        return access_token  # Return the access token
        return JsonResponse(response.json())
    else:
        # Handle the error case
        print('Failed to retrieve access token.')
        return None


def make_mpesa_express_request(request):
    shortcode = os.environ.get('BusinessShortCode')
    passkey = os.environ.get('PASS_KEY')

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password_data = f"{shortcode}{passkey}{timestamp}"
    password_bytes = base64.b64encode(password_data.encode("utf-8"))
    password = password_bytes.decode("utf-8")

    access_token = AccessToken.objects.first()
    if access_token is None or access_token.is_expired():
        access_token = get_access_token(request)
        if access_token:
            existing_token = AccessToken.objects.first()
            if existing_token:
                existing_token.token = access_token
                existing_token.save()
            else:
                AccessToken.objects.create(token=access_token)

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": os.environ.get('BusinessShortCode'),
        "Password": password,
        "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": '1',
        "PartyA": "254702855081",
        "PartyB": os.environ.get('BusinessShortCode'),
        "PhoneNumber": "254722770727",
        "CallBackURL": "https://33a8-197-156-137-147.ngrok-free.app/api/transactions/mpesa_callback/",
        "AccountReference": "ostram",
        "TransactionDesc": "ostram"
    }

    response = requests.post(api_url, headers=headers,
                             data=json.dumps(payload))

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse(response.json())


@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':

        result_body = request.body.decode('utf-8')

        result_json = json.loads(result_body)
        merchant_request_id = result_json['Body']['stkCallback']['MerchantRequestID']
        checkout_request_id = result_json['Body']['stkCallback']['CheckoutRequestID']
        result_code = result_json['Body']['stkCallback']['ResultCode']
        result_desc = result_json['Body']['stkCallback']['ResultDesc']
        callback_metadata = result_json['Body']['stkCallback']['CallbackMetadata']

        items = callback_metadata['Item']

        amount = None
        mpesa_receipt_number = None
        transaction_date = None
        phone_number = None
        for item in items:
            if item['Name'] == 'Amount':
                amount = float(item['Value'])
            elif item['Name'] == 'MpesaReceiptNumber':
                mpesa_receipt_number = item['Value']
            elif item['Name'] == 'TransactionDate':
                transaction_date = datetime.strptime(
                    str(item['Value']), "%Y%m%d%H%M%S")
                transaction_date = pytz.timezone(
                    'Africa/Nairobi').localize(transaction_date)
            elif item['Name'] == 'PhoneNumber':
                phone_number = item['Value']

        mpesa_callback = LipaNaMpesaCallback(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            result_code=result_code,
            result_desc=result_desc,
            amount=amount,
            mpesa_receipt_number=mpesa_receipt_number,
            transaction_date=transaction_date,
            phone_number=phone_number
        )
        mpesa_callback.save()

        # Return a response
        return HttpResponse('Callback received successfully')

    # Handle GET requests or other HTTP methods
    return HttpResponse('Invalid request')


def transaction_status(request):
    access_token = AccessToken.objects.first()
    if access_token is None or access_token.is_expired():
        access_token = get_access_token(request)
        if access_token:
            existing_token = AccessToken.objects.first()
            if existing_token:
                existing_token.token = access_token
                existing_token.save()
            else:
                AccessToken.objects.create(token=access_token)

    api_url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "Initiator": "njoro410",
        "SecurityCredential": "OANvCkI0XxUo9rwmIP31lAxUbCmCBA4iWfOfH5L2WOENtDMDXowdrj0EfkYLPx68okHRUeZPeiaezI8SG8NA4hro/vltJVRJFDT/fX6emLEFVSNX8zoZDk/SzRsoSYynDZ9DAy9wrTpnkCwN3o8LZwaKkNzvD/DhbvaRXTPvFrGNXR441TmaGpSliS3tDk6fZ/4TIdmbabWTePYMDSwWr9X+P5O66lx+W8hViORiBJcOanGSOQI1b4P4680hc9We3tcE7Z0U1q0RQPeYXZXphRs++CaDR7XqmxeiQkazpmqUh5bF6b1Nymum+pwqgpux9hYRkOE7oWJ20MB5qoj9lg==",
        "CommandID": "TransactionStatusQuery",
        "TransactionID": "RGF0LLBYLW",
        "OriginatorConversationID":"",
        "PartyA": '174379',
        "IdentifierType": "4",
        "ResultURL": "https://33a8-197-156-137-147.ngrok-free.app/api/transactions/transaction_status_callback/",
        "QueueTimeOutURL": "https://mydomain.com/TransactionStatus/queue/",
        "Remarks": "bla bla bla bla",
        "Occassion": "bla bla bla bla bla",
    }

    response = requests.post(api_url, headers=headers,
                             data=json.dumps(payload))

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse(response.json())


@csrf_exempt
def transaction_status_callback(request):
    if request.method == 'POST':
        result_body = request.body.decode('utf-8')
        print("transaction_status_callback::::",result_body)
        data = json.loads(result_body)

        # Extract values from the JSON
        conversation_id = data['Result']['ConversationID']
        originator_conversation_id = data['Result']['OriginatorConversationID']
        reference_item_key = data['Result']['ReferenceData']['ReferenceItem']['Key']
        result_code = data['Result']['ResultCode']
        result_desc = data['Result']['ResultDesc']
        result_type = data['Result']['ResultType']
        transaction_id = data['Result']['TransactionID']

        # Save the extracted values in the database
        # Result.objects.create(
        #     conversation_id=conversation_id,
        #     originator_conversation_id=originator_conversation_id,
        #     reference_item_key=reference_item_key,
        #     result_code=result_code,
        #     result_desc=result_desc,
        #     result_type=result_type,
        #     transaction_id=transaction_id
        # )

        return HttpResponse('Callback received successfully')

    return HttpResponse('Invalid request')


def c2b_confirmation_register(request):
    access_token = AccessToken.objects.first()
    if access_token is None or access_token.is_expired():
        access_token = get_access_token(request)
        if access_token:
            existing_token = AccessToken.objects.first()
            if existing_token:
                existing_token.token = access_token
                existing_token.save()
            else:
                AccessToken.objects.create(token=access_token)

    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "ShortCode": '174379',
        "ResponseType": "Completed",
        "ConfirmationURL": "https://33a8-197-156-137-147.ngrok-free.app/api/transactions/c2b_confirmation_callback",
        "ValidationURL": "https://33a8-197-156-137-147.ngrok-free.app/api/transactions/c2b_confirmation_validation",
    }

    response = requests.post(api_url, headers=headers,
                             data=json.dumps(payload))

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse(response.json())
    
    

@csrf_exempt
def c2b_confirmation_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        
        transaction = Transaction(
            transaction_type=data.get('TransactionType'),
            transaction_id=data.get('TransID'),
            transaction_time=data.get('TransTime'),
            transaction_amount=data.get('TransAmount'),
            business_short_code=data.get('BusinessShortCode'),
            bill_ref_number=data.get('BillRefNumber'),
            invoice_number=data.get('InvoiceNumber'),
            org_account_balance=data.get('OrgAccountBalance'),
            third_party_trans_id=data.get('ThirdPartyTransID'),
            msisdn=data.get('MSISDN'),
            first_name=data.get('FirstName'),
            middle_name=data.get('MiddleName'),
            last_name=data.get('LastName')
        )
        
        transaction.save()
        
        return HttpResponse('Callback received and transaction details saved successfully.')

    # Handle GET requests or other HTTP methods
    return HttpResponse('Invalid request')


@csrf_exempt
def c2b_confirmation_validation(request):
    if request.method == 'POST':
        result_body = request.body.decode('utf-8')
        # print(result_body)
        
        return HttpResponse('Validation')

    # Handle GET requests or other HTTP methods
    return HttpResponse('Invalid request')