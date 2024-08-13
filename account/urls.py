from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html',email_template_name='account/password_reset_email.html',success_url='/account/password_reset/done/'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), 
        name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html', success_url='/account/reset/done/'), 
        name='password_reset_confirm'),
]
