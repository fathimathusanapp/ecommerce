from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from .forms import AddressForm
from admin_panel.models import CustomUser
from .models import Address
from django.urls import reverse

import random

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('account:register')

        otp = random.randint(100000, 999999)
        request.session['registration_data'] = {
            'email': email,
            'username': username,
            'password': password,
            'otp': otp
        }

        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            settings.EMAIL_HOST_USER,
            [email],
        )
        messages.success(request, "OTP sent to your email.")
        return redirect('account:verify_otp')

    return render(request, 'account/register.html')

from django.db import IntegrityError

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        registration_data = request.session.get('registration_data')

        if registration_data:
            if str(entered_otp) == str(registration_data['otp']):
                # Check if the username or email already exists
                if CustomUser.objects.filter(username=registration_data['username']).exists():
                    messages.error(request, "Username already exists. Please try again with a different username.")
                    return redirect('account:register')
                if CustomUser.objects.filter(email=registration_data['email']).exists():
                    messages.error(request, "Email already exists. Please try again with a different email.")
                    return redirect('account:register')

                # Create the user
                try:
                    CustomUser.objects.create_user(
                        username=registration_data['username'],
                        email=registration_data['email'],
                        password=registration_data['password']
                    )
                    messages.success(request, "Registration successful!")
                    del request.session['registration_data']
                    return redirect('account:login')
                except IntegrityError as e:
                    messages.error(request, "An error occurred during registration. Please try again.")
                    return redirect('account:register')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        else:
            messages.error(request, "Session expired. Please register again.")
            return redirect('account:register')

    return render(request, 'account/verify_otp.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home:index')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home:index')

@login_required(login_url='account:login')
def profile_view(request):
    user = request.user

    if request.method == "POST":
        if 'add_address' in request.POST:
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = user
                address.save()
                return redirect('account:profile')

        elif 'delete_address' in request.POST:
            address_id = request.POST.get('address_id')
            address = get_object_or_404(Address, id=address_id, user=user)
            address.delete()
            return redirect('account:profile')
    else:
        form = AddressForm()

    context = {
        'user': user,
        'address_form': form,
    }
    return render(request, 'account/profile.html', context)

def add_address(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            street=request.POST['street'],
            city=request.POST['city'],
            state=request.POST['state'],
            zipcode=request.POST['zipcode'],
            phone_number=request.POST['phone_number']
        )
        return redirect('profile')
    return render(request, 'account/add_address.html')

def delete_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    address.delete()
    return redirect('profile')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "account/password_reset_email.html"
                    context = {
                        "email": user.email,
                        "domain": get_current_site(request).domain,
                        "site_name": "SnugBee",  # Replace with your site name
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": "https" if request.is_secure() else "http",
                    }
                    email_content = render_to_string(email_template_name, context)
                    send_mail(
                        subject,
                        email_content,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                messages.success(request, "A password reset link has been sent to your email.")
                return redirect('account:login')  # Update URL name as needed
            else:
                messages.error(request, "No user is associated with this email.")
    else:
        form = PasswordResetForm()
    return render(request, 'account/password_reset.html', {'form': form})

# Password Reset Confirm View
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(CustomUser, pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        messages.error(request, f"An error occurred: {e}")
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been successfully reset!")
                return redirect('account:login')  # Update URL name as needed
        else:
            form = SetPasswordForm(user)
        return render(request, 'account/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('account:password_reset')  # Update URL name as needed

# Password Reset Done View
def password_reset_done(request):
    return render(request, 'account/password_reset_done.html')

# Password Reset Complete View
def password_reset_complete(request):
    return render(request, 'account/password_reset_complete.html')

@login_required(login_url='account:login')
@login_required
def user_dashboard(request):
    return render(request, 'account/userdashboard.html')