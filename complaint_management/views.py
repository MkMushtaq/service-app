import csv

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from twilio.base.exceptions import TwilioRestException

from service.models import ComplaintDetail
from datetime import datetime
from .filters import ComplaintFilter
from django.contrib.admin.views.decorators import staff_member_required
from .form import CompliantUpdateForm
from twilio.rest import Client
from datetime import timedelta
import requests, json



@login_required
def view_complaints(request):
    all_complaints = ComplaintDetail.objects.all().order_by('-requested_date')

    filter_form = ComplaintFilter(request.GET, queryset=all_complaints)
    complaints = filter_form.qs
    context = {
        'just_arrived_number': all_complaints.filter(status='Just Arrived').count(),
        'active_complaints_number': all_complaints.filter(status='On Going').count(),
        'pending_complaints_number': all_complaints.filter(status='Pending').count(),
        'closed_complaints_number': all_complaints.filter(status='Closed').count(),
        'total_complaints_number': all_complaints.count(),
        'current_date': datetime.now().date(),
        'all_complaints': all_complaints,
        'complaints': complaints,
        'filter_form': filter_form
    }
    return render(request, 'complaint_management/complaints.html', context=context)


@login_required
def export_csv(request):
    print('Function Being Called')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=complaints.csv'

    columns = ['Complaint ID', 'Customer Name', 'Customer Mobile', 'Invoice Number', 'Service Requirement',
               'Customer Address', 'Requested Date', 'Technician Assigned', 'Current Technician',
               'Diagnosis Description', 'Status', 'Material Purchased', 'Price of Materials', 'Price Charged',
               'Payment Advance']

    writer = csv.writer(response)
    writer.writerow(columns)

    all_complaints = ComplaintDetail.objects.all()
    filter_form = ComplaintFilter(request.GET, queryset=all_complaints)
    complaints = filter_form.qs

    for complaint in complaints:
        date_str = str(complaint.requested_date + timedelta(hours = 5, minutes = 30))[:19]

        row = [complaint.id, complaint.customer_name, complaint.customer_mobile, complaint.invoice_number,
               complaint.service_requirement,
               complaint.customer_address, datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"), complaint.technician_assigned,
               complaint.current_technician,
               complaint.diagnosis_description, complaint.status, complaint.material_purchased,
               complaint.price_of_materials,
               complaint.price_charged, complaint.payment_advance]
        writer.writerow(row)

    return response


@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'complaint_management/logout.html')


@staff_member_required
def admin_logout(request):
    auth.logout(request)
    return render(request, 'complaint_management/logout_admin.html')


def login_request_admin(request):
    if request.user.is_authenticated:
        return redirect("view_complaints_admin_page")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("view_complaints_admin_page")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="complaint_management/login_admin.html", context={"login_form": form})


@login_required
@staff_member_required
def view_complaints_admin(request):
    if request.user.is_authenticated:

        all_complaints = ComplaintDetail.objects.all().order_by('-requested_date')
        filter_form = ComplaintFilter(request.GET, queryset=all_complaints)
        complaints = filter_form.qs

        context = {
            'just_arrived_number': all_complaints.filter(status='Just Arrived').count(),
            'active_complaints_number': all_complaints.filter(status='On Going').count(),
            'pending_complaints_number': all_complaints.filter(status='Pending').count(),
            'closed_complaints_number': all_complaints.filter(status='Closed').count(),
            'total_complaints_number': all_complaints.count(),
            'current_date': datetime.now().date(),
            'all_complaints': all_complaints,
            'complaints': complaints,
            'filter_form': filter_form,
        }

        return render(request, 'complaint_management/complaints_admin.html', context=context)

    else:
        return redirect("complaint_info_login_admin_page")


@staff_member_required
def update_complaint_details(request, pk):
    complaint = ComplaintDetail.objects.get(id=pk)
    update_form = CompliantUpdateForm(instance=complaint)
    prev_status = complaint.status


    update_form.fields['requested_date'].widget.attrs['readonly'] = True
    if request.method == "POST":

        update_form = CompliantUpdateForm(request.POST, instance=complaint)
        if update_form.is_valid():
            account_sid = os.getenv('F2SMS_SID')
            auth_token = os.getenv('F2SMS_AUTH_TOKEN')
            lient = Client(account_sid, auth_token)
            technician_num = update_form.cleaned_data['technician_mobile']
            technician_name = update_form.cleaned_data['technician_assigned']
            customer_num = update_form.cleaned_data['customer_mobile']
            customer_name = update_form.cleaned_data['customer_name']
            customer_address = update_form.cleaned_data['customer_address']

            numbers = [customer_num, technician_num, '7729988320']

            admins = ['7729988320']
            if update_form.cleaned_data['status'] == 'On Going' and prev_status != 'On Going':
                for number in numbers:
                    if number in admins:
                        msg = "Complaint assigned. \n\nCustomer name: " + \
                              update_form.cleaned_data['customer_name'] + \
                              "\nTechnician Name: " + update_form.cleaned_data['technician_assigned']

                    elif number == customer_num:
                        msg = "Dear Customer, \n\nTechnician " + technician_name + \
                              " is on his way. \n\n Technician Contact: " + technician_num \
                                                + "\n\nTeam Airngas"
                    elif number == technician_num:
                        msg = "Customer Details:- \n\nCustomer name:" + customer_name + \
                                            "\nCustomer Phone:" + customer_num + \
                                            "\nCustomer Address:" + customer_address

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

                        messages.error(request, 'Invalid Technician Number')
                        return HttpResponseRedirect(request.path_info)
                update_form.save()


            if update_form.cleaned_data['status'] == 'Closed' and prev_status != 'Closed':
                for number in numbers:
                    if number in admins:
                        msg = "Complaint closed. \n\nCustomer name: " + \
                              update_form.cleaned_data['customer_name']
                    elif number == customer_num:
                        msg = "Dear Customer, \n\nYour complaint has been successfully resolved.\
                         Thank you for using our services. \n\nTeam Airngas"
                    else:
                        continue

                    url = "https://www.fast2sms.com/dev/bulk"
                    payload = "sender_id=FSTSMS&message=" + msg + "&language=english&route=p&numbers="+number
                    headers = {
                    'authorization': "Rh8KFX4OmYNMlZ6razVLiQbgy3GwDjWxpU7P9uC51t2JqesSIo9JyzW4cn8LbOmY3takIwlQoqAeRSXZ",
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache",
                    }
                    response = requests.request("POST", url, data=payload, headers=headers)
                    print(response.text)
                update_form.save()

            update_form.save()
            return redirect('view_complaints_admin_page')

    context = {
        'update_form': update_form
    }
    return render(request, 'complaint_management/update_complaints.html', context=context)
