from django.urls import path
from . import views

app_name = 'ad'

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('<str:adtype>/', views.create_ad, name='create_ad'),
]