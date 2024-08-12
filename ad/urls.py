from django.urls import path
from . import views

app_name = 'ad'

urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('<str:adtype>/', views.AdCreateView.as_view(), name='create_ad'),
    path('<str:adtype>/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('<str:adtype>/<int:pk>/update/', views.AdUpdateView.as_view(), name='ad_update'),
    path('<str:adtype>/<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),
]