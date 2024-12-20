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
from .models import UserProfile, NOCRequest,LORRequest, NoDueSlip
from django.http import HttpResponse


def generate_otp():
    """Generate a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('users:signup')

        # Generate an OTP and send it to the email
        otp = generate_otp()
        request.session['otp'] = otp  # Store OTP in session for verification
        request.session['email'] = email  # Store email in session
        request.session['password'] = password  # Store password in session
        request.session['name'] = username  # Store name in session

        # Sending the OTP email
        send_mail(
            'Your Account Verification OTP',
            f'Your OTP for account verification is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        # Redirect to verify OTP page
        return redirect('users:verify_otp')

    return render(request, 'users/signup.html', {'MEDIA_URL': settings.MEDIA_URL})


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        generated_otp = request.session.get('otp')
        email = request.session.get('email')
        password = request.session.get('password')
        name = request.session.get('name')

        if entered_otp == generated_otp:
            # OTP is correct, save the user to the database
            if not UserProfile.objects.filter(email=email).exists():
                user = UserProfile(name=name, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully.")
                return redirect('users:login')
            else:
                messages.error(request, "An account with this email already exists.")
                return redirect('users:signup')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('users:verify_otp')

    return render(request, 'users/verify_otp.html', {'MEDIA_URL': settings.MEDIA_URL})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Manually authenticate the user using UserProfile model
        try:
            user_profile = UserProfile.objects.get(email=username)  # Assuming username is the email
            if user_profile.password == password:  # Verify password
                # Login logic: Create a session manually
                request.session['user_id'] = user_profile.id  # Store the user ID in the session
                request.session['username'] = user_profile.name  # Store the username in session
                
                messages.success(request, 'You are now logged in!')
                return redirect('users:dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html')

# def dashboard(request):
#     if request.user.is_authenticated:
#         return render(request, 'users/dashboard/student_dashboard.html')
#     else:
#         return redirect('users:login')

def dashboard(request):
    return render(request, 'users/dashboard/student_dashboard.html', {'MEDIA_URL': settings.MEDIA_URL})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            # Check if a user with this email exists in UserProfile model
            user_profile = UserProfile.objects.get(email=email)
            
            # Generate a random reset token
            reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            
            # Save the token in the session for later verification
            request.session['reset_token'] = reset_token
            request.session['reset_email'] = email
            
            # Construct the reset URL (assuming you have a 'reset_password' view)
            reset_url = request.build_absolute_uri(reverse('users:reset_password') + f"?token={reset_token}")
            
            # Send email with the reset URL
            send_mail(
                'Password Reset Request',
                f'Hello, please use the following link to reset your password: {reset_url}',
                'support@example.com',  # Replace with your support email
                [email],
                fail_silently=False,
            )
            
            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('users:login')
        
        except UserProfile.DoesNotExist:
            messages.error(request, "No account found with that email address.")
            return redirect('users:forgot-password')

    return render(request, 'users/forgot-password.html', {'MEDIA_URL': settings.MEDIA_URL})

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        token = request.GET.get('token')
        email = request.session.get('reset_email')

        # Validate the token and email
        if token == request.session.get('reset_token') and email:
            try:
                user_profile = UserProfile.objects.get(email=email)
                # Update the password
                user_profile.password = new_password  # You should hash the password before saving
                user_profile.save()
                
                # Clear the session
                del request.session['reset_token']
                del request.session['reset_email']
                
                messages.success(request, "Your password has been reset successfully.")
                return redirect('users:login')
            
            except UserProfile.DoesNotExist:
                messages.error(request, "Invalid reset token or email.")
                return redirect('users:forgot_password')
        
        else:
            messages.error(request, "Invalid reset token.")
            return redirect('users:forgot_password')

    return render(request, 'users/reset_password.html')

# Function to submit NOC request
def noc_request(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        roll_no = request.POST.get('roll_no')  # Get roll number from form
        email = request.POST.get('email')  # Assume email is provided in the POST request
        request_description = request.POST.get('request_description')
        google_drive_link = request.POST.get('google_drive_link')
        
        # Get the UserProfile instance using the email (foreign key)
        try:
            user_profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return HttpResponse("User with this email does not exist.", status=400)
        
        # Create and save the NOCRequest
        noc_request = NOCRequest(
            student_name=student_name,
            roll_no=roll_no,  # Save the roll number
            email=user_profile,  # ForeignKey relation
            request_description=request_description,
            google_drive_link=google_drive_link
        )
        noc_request.save()
        
        return redirect('users:success_page')  # Redirect to a success page (you can customize this)

    return render(request, 'users/dashboard/noc_request.html', {'MEDIA_URL': settings.MEDIA_URL})

# # Function to submit No Due Slip
# def no_due_slip(request):
#     if request.method == 'POST':
#         student_name = request.POST.get('student_name')
#         roll_no = request.POST.get('roll_no')  # Get roll number from form
#         email = request.POST.get('email')  # Assume email is provided in the POST request
#         request_description = request.POST.get('request_description')
#         google_drive_link = request.POST.get('google_drive_link')

#         # Get the UserProfile instance using the email (foreign key)
#         try:
#             user_profile = UserProfile.objects.get(email=email)
#         except UserProfile.DoesNotExist:
#             return HttpResponse("User with this email does not exist.", status=400)

#         # Create and save the NoDueSlip
#         no_due_slip = NoDueSlip(
#             student_name=student_name,
#             roll_no=roll_no,  # Save the roll number
#             email=user_profile,  # ForeignKey relation
#             request_description=request_description,
#             google_drive_link=google_drive_link
#         )
#         no_due_slip.save()

#         return redirect('users:success_page')  # Redirect to a success page (you can customize this)

#     return render(request, 'users/dashboard/no_due_slip.html', {'MEDIA_URL': settings.MEDIA_URL})

def no_due_slip(request):
    if request.method == 'POST':
        # Get data from the form
        student_name = request.POST.get('student_name')
        roll_no = request.POST.get('roll_no')
        email = request.POST.get('email')  # Assuming email is provided in the POST request
        hostel = request.POST.get('hostel', 'Hostel Name Not Provided')  # Default if not provided
        room_no = request.POST.get('room_no', 'Room Number Not Provided')  # Default if not provided

        # Get the UserProfile instance using the email (foreign key relation)
        try:
            user_profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return HttpResponse("User with this email does not exist.", status=400)

        # Create and save the NoDueSlip instance
        no_due_slip = NoDueSlip(
            student_name=student_name,
            roll_no=roll_no,  # Save the roll number
            email=email,  # Storing email directly
            hostel=hostel,  # Save hostel information
            room_no=room_no,  # Save room number
        )
        no_due_slip.save()

        # Redirect to success page after saving
        return redirect('users:success_page')  # Redirect to a success page or an appropriate view

    return render(request, 'users/dashboard/no_due_slip.html', {'MEDIA_URL': settings.MEDIA_URL})

# Function to submit LOR request
def lor_request(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        roll_no = request.POST.get('roll_no')  # Get roll number from form
        email = request.POST.get('email')  # Assume email is provided in the POST request
        request_description = request.POST.get('request_description')
        google_drive_link = request.POST.get('google_drive_link')

        # Get the UserProfile instance using the email (foreign key)
        try:
            user_profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return HttpResponse("User with this email does not exist.", status=400)

        # Create and save the LORRequest
        lor_request = LORRequest(
            student_name=student_name,
            roll_no=roll_no,  # Save the roll number
            email=user_profile,  # ForeignKey relation
            request_description=request_description,
            google_drive_link=google_drive_link
        )
        lor_request.save()

        return redirect('users:success_page')  # Redirect to a success page (you can customize this)

    return render(request, 'users/dashboard/lor_request.html', {'MEDIA_URL': settings.MEDIA_URL})

def success_page(request):
    return render(request, 'users/dashboard/success_page.html')

# def track_request(request):
#     return render(request, 'users/dashboard/track_request.html', {'MEDIA_URL': settings.MEDIA_URL})

def track_request(request):
    # Fetch the data from the models
    noc_requests = NOCRequest.objects.all()  # Get all NOC requests
    no_due_slips = NoDueSlip.objects.all()  # Get all No Due Slips
    lor_requests = LORRequest.objects.all()  # Get all LOR requests
    
    # Pass the data to the template
    context = {
        'noc_requests': noc_requests,
        'no_due_slips': no_due_slips,
        'lor_requests': lor_requests,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    
    return render(request, 'users/dashboard/track_request.html', context) # for specific logged in user only