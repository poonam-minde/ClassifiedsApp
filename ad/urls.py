from django.urls import path
from . import views

app_name = 'ad'

urlpatterns = [
    path('', views.AllAdListView.as_view(), name='all_ad_list'),
    path('job/', views.JobListView.as_view(), name='job_list'),
    path('sale/', views.SaleListView.as_view(), name='sale_list'),
    path('rental/', views.RentalListView.as_view(), name='rental_list'),
    path('service/', views.ServiceListView.as_view(), name='service_list'),
    path('event/', views.EventListView.as_view(), name='event_list'),
    path('class/', views.ClassListView.as_view(), name='class_list'),
    path('ad/', views.AdListView.as_view(), name='ad_list'),
    path('ad/<str:adtype>/', views.AdCreateView.as_view(), name='create_ad'),
    path('ad/<str:adtype>/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/<str:adtype>/<int:pk>/update/', views.AdUpdateView.as_view(), name='ad_update'),
    path('ad/<str:adtype>/<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),
]