from django.urls import path
from . import views

app_name = 'ad'

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('<str:adtype>/', views.AdCreateView.as_view(), name='create_ad'),
]