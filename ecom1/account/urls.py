from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   
    path('profile/', views.profile_view, name='profile'),
    
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('complete/', views.password_reset_complete, name='password_reset_complete'),

    path('userdashboard/', views.user_dashboard, name='userdashboard'),
]