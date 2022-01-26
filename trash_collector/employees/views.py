from datetime import date
from time import strftime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


#from trash_collector.customers.models import Customer

from .models import Employee

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.
@login_required
def index(request, day=date.today().strftime('%A')):
    Customer = apps.get_model('customers.Customer') 
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        todays_date = date.today()
        todays_date = todays_date if day == todays_date.strftime('%A') else date(1892,1,1)

        todays_customers = Customer.objects.filter(Q(zip_code=logged_in_employee.zip_code), Q(one_time_pickup=todays_date) | Q(weekly_pickup=day)).exclude(suspend_start__lte=todays_date, suspend_end__gte=todays_date).exclude(date_of_last_pickup=todays_date)

        context = {
            'logged_in_employee': logged_in_employee,
            'today': day,
            'customers': todays_customers
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

def confirm_pickup(request, id):
    Customer = apps.get_model('customers.Customer')
    customer = Customer.objects.get(pk=id)
    customer.date_of_last_pickup = date.today()
    customer.balance += 20
    customer.save()
    return HttpResponseRedirect(reverse('employees:index'))

def select_day(request, day): # FIXME: REFACTOR INTO index.html
    Customer = apps.get_model('customers.Customer') 
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        todays_date = date.today()
        todays_date = todays_date if day == todays_date.strftime('%A') else date(1892,1,1)

        todays_customers = Customer.objects.filter(Q(zip_code=logged_in_employee.zip_code), Q(one_time_pickup=todays_date) | Q(weekly_pickup=day)).exclude(suspend_start__lte=todays_date, suspend_end__gte=todays_date).exclude(date_of_last_pickup=todays_date)

        context = {
            'logged_in_employee': logged_in_employee,
            'today': day,
            'customers': todays_customers
        }
        return render(request, 'employees/select_day.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))
    # return HttpResponseRedirect(reverse('employees:index', args=(day,)))

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
