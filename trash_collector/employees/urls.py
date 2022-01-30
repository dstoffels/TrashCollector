from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('confirm_pickup/<int:id>/<str:selected_date>', views.confirm_pickup, name="confirm_pickup"),
    path('select_day/<str:day>/', views.select_day, name="select_day"),
    path('details/<int:id>/', views.customer_details, name="details"),
    path('toggle_pickups/<str:day>', views.toggle_pickups, name='toggle_pickups')
]