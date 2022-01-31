from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import Employee

from .helpers import parse_date
import gmaps_api

# Create your views here.
anchor = ''

@login_required
def index(request):
    global anchor
    anchor = ''
    today = date.today()
    return HttpResponseRedirect(reverse('employees:select_day', args=(today,)))

def confirm_pickup(request, id, selected_date):
    Customer = apps.get_model('customers.Customer')
    customer = Customer.objects.get(pk=id)
    customer.date_of_last_pickup = selected_date
    customer.balance += 20
    customer.save()
    global anchor 
    anchor = 'index-table'
    return HttpResponseRedirect(reverse('employees:select_day', args=(selected_date,)))

def select_day(request, day=''):
    Customer = apps.get_model('customers.Customer')

    display_date = parse_date(request.POST['selected_date']) if request.method == 'POST' else parse_date(day)
    day = display_date.strftime("%A")
    global anchor

    try:
        logged_in_employee = Employee.objects.get(user = request.user)
        todays_customers = Customer.objects.filter(Q(zip_code=logged_in_employee.zip_code), Q(one_time_pickup=display_date) | Q(weekly_pickup=day)).exclude(suspend_start__lte=display_date, suspend_end__gte=display_date).order_by('last_name')
        for customer in todays_customers:
            customer.confirm_pickup(display_date)
        
        context = {
            'logged_in_employee': logged_in_employee,
            'customers': todays_customers,
            'today': day,
            'selected_date': display_date,
            'anchor': anchor,
            'gmaps': gmaps_api.LINK,
            'center': gmaps_api.average_latlng(todays_customers, logged_in_employee.zip_code)
        }

        anchor = ''
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))


def toggle_pickups(request, day):
    logged_in_employee: Employee = Employee.objects.get(user = request.user)
    logged_in_employee.toggle_pickups()
    global anchor 
    anchor = 'index-table'
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
