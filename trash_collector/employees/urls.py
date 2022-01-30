from django.urls import path

from . import views

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('<int:id>/<str:selected_date>/confirm_pickup/', views.confirm_pickup, name="confirm_pickup"),
    path('select_day/<str:day>/', views.select_day, name="select_day"),
    path('<int:id>/details/', views.customer_details, name="details"),
    path('toggle_pickups/<str:day>', views.toggle_pickups, name='toggle_pickups')
]