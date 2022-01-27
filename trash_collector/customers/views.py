from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date

from .models import Customer
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from api_keys import STRIPE_TEST_API_KEY


@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_customer = Customer.objects.get(user=logged_in_user)

        today = date.today()
        
        context = {
            'logged_in_customer': logged_in_customer,
            'today': today
        }
        return render(request, 'customers/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('customers:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        weekly_from_form = request.POST.get('weekly_pickup')
        new_customer = Customer(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form, weekly_pickup=weekly_from_form)
        new_customer.convert_address()
        new_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/create.html')

@login_required
def suspend_service(request):
    logged_in_user = request.user
    logged_in_customer = Customer.objects.get(user=logged_in_user)
    if request.method == "POST":
        start_from_form = request.POST.get('start')
        end_from_form = request.POST.get('end')
        logged_in_customer.suspend_start = start_from_form
        logged_in_customer.suspend_end = end_from_form
        logged_in_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        context = {
            'logged_in_customer': logged_in_customer
        }
        return render(request, 'customers/suspend.html', context)

@login_required
def one_time_pickup(request):
    logged_in_user = request.user
    logged_in_customer = Customer.objects.get(user=logged_in_user)
    if request.method == "POST":
        date_from_form = request.POST.get('date')
        logged_in_customer.one_time_pickup = date_from_form
        logged_in_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        context = {
            'logged_in_customer': logged_in_customer
        }
        return render(request, 'customers/one_time.html', context)

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_customer = Customer.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        weekly_pickup_from_form = request.POST.get('weekly')
        logged_in_customer.name = name_from_form
        logged_in_customer.address = address_from_form
        logged_in_customer.zip_code = zip_from_form
        logged_in_customer.weekly_pickup = weekly_pickup_from_form
        logged_in_customer.convert_address()
        logged_in_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        context = {
            'logged_in_customer': logged_in_customer
        }
        return render(request, 'customers/edit_profile.html', context)

@login_required
def checkout(request):
    logged_in_user = request.user
    logged_in_customer = Customer.objects.get(user=logged_in_user)
    return render(request, 'customers/checkout.html')


def success(request):
    pass


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


@csrf_exempt
def create_payment(request):
        stripe.api_key = STRIPE_TEST_API_KEY
    # try:
        # data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            payment_method_types = ['card'],
            amount=50,
            currency='usd',
            # automatic_payment_methods={
            #     'enabled': True,
            # },
        )
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    # except Exception as e:
    #     return JsonResponse({"error": str(e)}), 403