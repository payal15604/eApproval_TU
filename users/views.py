# users/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
import random

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        
        # Send OTP to the user's email
        otp = random.randint(100000, 999999)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'no-reply@university.com',
            [email],
            fail_silently=False,
        )
        
        # Store the OTP in the session
        request.session['otp'] = otp
        return redirect('verify_otp')
    
    return render(request, 'users/signup.html')


# users/views.py
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if int(entered_otp) == request.session.get('otp'):
            # OTP verified, create the user
            username = request.POST['username']
            email = request.POST['email']
            user = User.objects.create_user(username=username, email=email, password=request.POST['password'])
            user.save()
            messages.success(request, 'User registered successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'users/verify_otp.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'users/login.html')



def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'users/dashboard.html')
    else:
        return redirect('login')
