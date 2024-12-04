from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from ..forms import UserRegistrationForm
from ..models import User
import uuid

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # User won't be active until email is verified
            user.save()

            # Generate verification token
            token = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('user/email/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': token,
            })
            
            send_mail(
                subject,
                message,
                'noreply@pizzadelivery.com',
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Please check your email to activate your account.')
            return redirect('user_login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me', False)
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)  # Session expires when browser closes
                    return redirect('home')
                else:
                    messages.error(request, "Please verify your email address first.")
            else:
                messages.error(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email address")
    
    return render(request, 'user/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

def activate_account(request, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated. You can now login.")
        else:
            messages.info(request, "Your account is already activated.")
            
        return redirect('user_login')
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect('user_login')

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
                f'Your temporary password is: {temp_password}\nPlease login and change your password immediately.',
                'noreply@pizzadelivery.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'A temporary password has been sent to your email.')
            return redirect('user_login')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    
    return render(request, 'user/forgot_password.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')
            
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')
            
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Password successfully changed.')
        return redirect('user_login')
        
    return render(request, 'user/change_password.html')
