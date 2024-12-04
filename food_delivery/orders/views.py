from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserRegistrationForm
from .models import User
import uuid

def home(request):
    return render(request, 'index.html')  # Home page view

def about(request):
    return render(request, 'about.html')  # About page view


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            # Generate a temporary password
            temp_password = str(uuid.uuid4())[:8]
            user.set_password(temp_password)
            user.save()
            
            # Send email with temporary password
            send_mail(
                'Password Reset',
                f'Your temporary password is: {temp_password}\nPlease login and change your password.',
                'noreply@pizzadelivery.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'A temporary password has been sent to your email.')
            return redirect('user_login')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    
    return render(request, 'user/forgot_password.html')

def register(request):
    # This view will handle user registration and use a form
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            # Create the new user object
            user = form.save(commit=False)
            # Hash the password before saving
            user.set_password(form.cleaned_data['password'])
            user.save()  # Save the user to the database

            # Show success message
            messages.success(request, 'Registration successful. You can now log in.')
            
            return redirect('user_login')  # Redirect to login page

        else:
            # If the form is not valid, show error messages
            messages.error(request, 'Please correct the errors below.')

    else:
        form = UserRegistrationForm()  # Render empty form on GET request

    return render(request, 'user/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST['username']  # Form field is still named 'username'
        password = request.POST['password']
        
        try:
            # First get the user by email
            user = User.objects.get(email=email)
            # Then authenticate with email
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page or dashboard
            else:
                messages.error(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email address")
    
    return render(request, 'user/login.html')
