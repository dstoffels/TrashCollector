from datetime import date, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import Employee

import gmaps_api

# Create your views here.

def parse_date(day) -> date:
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if day in weekdays:
        todays_date = date.today()
        todays_index = todays_date.weekday()
        day_index = weekdays.index(day)
        difference = day_index - todays_index
        return date(todays_date.year, todays_date.month, todays_date.day + difference)
    else:
        return datetime.strptime(day, '%Y-%m-%d').date()

@login_required
def index(request):
    today = date.today()
    return HttpResponseRedirect(reverse('employees:select_day', args=(today,)))

def confirm_pickup(request, id):
    Customer = apps.get_model('customers.Customer')
    customer = Customer.objects.get(pk=id)
    customer.date_of_last_pickup = date.today()
    customer.balance += 20
    customer.save()
    return HttpResponseRedirect(reverse('employees:index'))

def select_day(request, day):
    Customer = apps.get_model('customers.Customer')
    display_date = parse_date(day)
    day = display_date.strftime("%A")
    try:
        logged_in_employee = Employee.objects.get(user = request.user)
        todays_customers = Customer.objects.filter(Q(zip_code=logged_in_employee.zip_code), Q(one_time_pickup=display_date) | Q(weekly_pickup=day)).exclude(suspend_start__lte=display_date, suspend_end__gte=display_date).exclude(date_of_last_pickup=display_date).order_by('last_name')
        context = {
            'logged_in_employee': logged_in_employee,
            'today': day,
            'customers': todays_customers,
            'gmaps': gmaps_api.LINK,
            'center': gmaps_api.average_latlng(todays_customers, logged_in_employee.zip_code)
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

def toggle_pickups(request, day):
    logged_in_employee: Employee = Employee.objects.get(user = request.user)
    logged_in_employee.toggle_pickups()
    return HttpResponseRedirect(reverse('employees:select_day', args=(day,)))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        first_name_from_form = request.POST.get('first_name')
        last_name_from_form = request.POST.get('last_name')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(first_name=first_name_from_form, last_name=last_name_from_form, user=logged_in_user, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        first_name_from_form = request.POST.get('first_name')
        last_name_from_form = request.POST.get('last_name')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.first_name = first_name_from_form
        logged_in_employee.last_name = last_name_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

@login_required
def customer_details(request, id):
    Customer = apps.get_model('customers.Customer') 
    customer = Customer.objects.get(pk=id)
    context = {
        'customer': customer,
        'gmaps': gmaps_api.LINK
    }
    return render(request, 'employees/details.html', context)
