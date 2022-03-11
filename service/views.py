from django.shortcuts import render, redirect
from twilio.base.exceptions import TwilioRestException
from django.contrib import messages
from .models import ComplaintDetail
from .form import ComplaintRequestForm
from twilio.rest import Client
import requests, json, os
# from sendsms import api
# from sendsms.message import SmsMessage
# from sms import send_sms


def display_service_page(request):
    form = ComplaintRequestForm(request.POST)
    context = {
        'form': form
    }
    return render(request, 'service/home.html', context=context)


def display_about_page(request):
    return render(request, 'service/about.html')


def display_services_page(request):
    return render(request, 'service/service.html')


def display_team_page(request):
    return render(request, 'service/team.html')


def display_success_page(request):
    return render(request, 'service/success.html')


def save_customer_details(request):
    if request.method == "POST":

        compliant_details = ComplaintRequestForm(request.POST)
        if compliant_details.is_valid():
            account_sid = os.getenv('F2SMS_SID')
            auth_token = os.getenv('F2SMS_AUTH_TOKEN')
            client = Client(account_sid, auth_token)

            numbers = [compliant_details.cleaned_data['customer_mobile'], '7729988320']
            admins = ['7729988320']

            for number in numbers:

                if number in admins:
                    name = compliant_details.cleaned_data['customer_name']
                    msg = 'New Complaint Registered.\n\nCustomer Name: ' + name + '\nPhone: ' + compliant_details.cleaned_data['customer_mobile']
                else:
                    msg = "Dear Customer, \n\nYour complaint has been successfully registered. Our technician will contact you soon. \n\nTeam Airngas"
                    print('Sending Message to Customer')
                
            
                print('n3', number)
                url = "https://www.fast2sms.com/dev/bulk"
                payload = "sender_id=FSTSMS&message=" + msg + "&language=english&route=p&numbers="+number
                headers = {
                'authorization': os.getenv('AUTHORIZATION'),
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
                }
                response = requests.request("POST", url, data=payload, headers=headers)
                print(response.text)
                response = json.loads(response.text)


                if response['message'] == "Invalid Numbers":
                    print('Exception raised')
                    print('n4', number)

                    messages.error(request, 'Invalid Phone Number')
                    return redirect('home_page')
                else:
                    compliant_details.save()

            return render(request, 'service/success.html')

    else:

        return render(request, 'service/home.html')
