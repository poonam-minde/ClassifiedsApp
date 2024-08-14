from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('', views.AllAdListView.as_view(), name='all_ad_list'),
    path('job/', views.JobListView.as_view(), name='job_list'),
    path('sale/', views.SaleListView.as_view(), name='sale_list'),
    path('rental/', views.RentalListView.as_view(), name='rental_list'),
    path('service/', views.ServiceListView.as_view(), name='service_list'),
    path('event/', views.EventListView.as_view(), name='event_list'),
    path('class/', views.ClassListView.as_view(), name='class_list'),
]