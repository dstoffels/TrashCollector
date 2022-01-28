from django.urls import path

from . import views

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('suspend/', views.suspend_service, name="suspend"),
    path('one_time/', views.one_time_pickup, name="one_time"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('checkout/', views.checkout, name="checkout"),
    path('create-payment-intent/', views.create_payment, name="create_payment"),
    path('success/', views.success, name='success')
]
