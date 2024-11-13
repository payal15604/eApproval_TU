# users/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.urls import reverse
import random
import string
# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         # Generate a random OTP
#         otp = random.randint(100000, 999999)
        
#         # Save OTP in session to access it later in verify_otp
#         request.session['otp'] = otp

#         # Send OTP to user’s email
#         send_mail(
#             'Your OTP Code',
#             f'Your OTP code is {otp}',
#             'software@example.com',  # Replace with your email
#             [email],
#             fail_silently=False,
#         )

#         # Save other data temporarily for verification
#         request.session['username'] = username
#         request.session['email'] = email
#         request.session['password'] = password
        
#         # Redirect to OTP verification page
#         return redirect('verify_otp')  # This assumes 'verify_otp' is mapped in your urls.py

#     return render(request, 'users/signup.html')

def generate_otp():
    """Generate a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Generate an OTP and send it to the Thapar email
        otp = generate_otp()
        request.session['otp'] = otp  # Store OTP in session for verification
        request.session['email'] = email  # Store email in session

        # Sending the OTP email
        send_mail(
            'Your Account Verification OTP',
            f'Your OTP for account verification is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        # Redirect to verify page
        return redirect('verify_otp')

    return render(request, 'users/signup.html', {'MEDIA_URL': settings.MEDIA_URL})

#working 
# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         # Generate a random OTP
#         otp = random.randint(100000, 999999)
        
#         # Save OTP in session to access it later in verify_otp
#         request.session['otp'] = otp

#         # Send OTP to user’s email
#         send_mail(
#             'Your OTP Code',
#             f'Your OTP code is {otp}',
#             'software@example.com',  # Replace with your email
#             [email],
#             fail_silently=False,
#         )

#         # Save other data temporarily for verification
#         request.session['username'] = username
#         request.session['email'] = email
#         request.session['password'] = password
        
#         # Redirect to OTP verification page
#         return redirect('verify_otp')  # This assumes 'verify_otp' is mapped in your urls.py

#     # Pass MEDIA_URL to the template
#     return render(request, 'users/signup.html', {'MEDIA_URL': settings.MEDIA_URL})

# # users/views.py
# def verify_otp(request):
#     if request.method == 'POST':
#         entered_otp = request.POST['otp']
#         if int(entered_otp) == request.session.get('otp'):
#             # OTP verified, create the user
#             username = request.POST['username']
#             email = request.POST['email']
#             user = User.objects.create_user(username=username, email=email, password=request.POST['password'])
#             user.save()
#             messages.success(request, 'User registered successfully!')
#             return redirect('login')
#         else:
#             messages.error(request, 'Invalid OTP')
#     return render(request, 'users/verify_otp.html')

# def verify_otp(request):
#     if request.method == 'POST':
#         entered_otp = request.POST['otp']
#         if int(entered_otp) == request.session.get('otp'):
#             username = request.POST['username']
#             email = request.POST['email']

#             # Check if username already exists
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username already exists. Please choose a different username.')
#                 return render(request, 'users/verify_otp.html')

#             # Create the user if username is unique
#             user = User.objects.create_user(username=username, email=email, password=request.POST['password'])
#             user.save()
#             messages.success(request, 'User registered successfully!')
#             return redirect('login')
#         else:
#             messages.error(request, 'Invalid OTP')
#     return render(request, 'users/verify_otp.html')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        generated_otp = request.session.get('otp')
        email = request.session.get('email')
        password = request.session.get('password')

        if entered_otp == generated_otp:
            # OTP is correct, create the user account
            if not User.objects.filter(username=email).exists():
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully.")
                return redirect('login')
            else:
                messages.error(request, "An account with this email already exists.")
                return redirect('signup')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')

    return render(request, 'users/verify_otp.html', {'MEDIA_URL': settings.MEDIA_URL})

# def verify_otp(request):
#     if request.method == 'POST':
#         entered_otp = request.POST.get('otp')
        
#         # Retrieve OTP and user details from the session
#         session_otp = request.session.get('otp')
#         username = request.session.get('username')
#         email = request.session.get('email')
#         password = request.session.get('password')
        
#         # Debug: Print to ensure session data is available
#         print(f"Session OTP: {session_otp}")
#         print(f"Session Username: {username}")
#         print(f"Session Email: {email}")
#         print(f"Session Password: {password}")
        
#         if entered_otp and session_otp and int(entered_otp) == session_otp:
#             # Check if the username already exists
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username already exists. Please choose a different username.')
#                 return render(request, 'users/verify_otp.html')

#             # Create the user if username is unique
#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.save()
#             messages.success(request, 'User registered successfully!')
#             return redirect('users:login')  # Redirect to login page
#         else:
#             messages.error(request, 'Invalid OTP')
            
#     # Render the OTP verification page
#     return render(request, 'users/verify_otp.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        # If authentication is successful, login the user
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('login')  # Update with the correct redirect path
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html', {'MEDIA_URL': settings.MEDIA_URL})

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'users/dashboard.html')
    else:
        return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            # Check if a user with this email exists
            user = User.objects.get(email=email)
            
            # Generate a random reset token
            reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            
            # Ideally, save this token in a model or in a session for security
            request.session['reset_token'] = reset_token
            request.session['reset_email'] = email
            
            # Construct reset URL (assuming a 'reset_password' view and URL name)
            reset_url = request.build_absolute_uri(reverse('reset_password') + f"?token={reset_token}")
            
            # Send email with reset link
            send_mail(
                'Password Reset Request',
                f'Hello, please use the following link to reset your password: {reset_url}',
                'support@example.com',  # Replace with your support email
                [email],
                fail_silently=False,
            )
            
            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('login')
        
        except User.DoesNotExist:
            messages.error(request, "No account found with that email address.")
            return redirect('forgot-password')

    return render(request, 'users/forgot-password.html', {'MEDIA_URL': settings.MEDIA_URL})



