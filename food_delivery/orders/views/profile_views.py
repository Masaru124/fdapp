from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import UserProfileForm
from ..models import User

@login_required
def profile(request):
    """View for displaying and updating user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'user/profile.html', context)

@login_required
def delete_account(request):
    """View for handling account deletion"""
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Verify password before deletion
        if request.user.check_password(password):
            user = request.user
            user.delete()
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password. Account deletion failed.')
            return redirect('delete_account')
            
    return render(request, 'user/delete_account.html')

@login_required
def manage_sessions(request):
    """View for managing user sessions"""
    if request.method == 'POST':
        # Delete all other sessions
        request.user.session_set.exclude(session_key=request.session.session_key).delete()
        messages.success(request, 'All other sessions have been terminated.')
        return redirect('manage_sessions')
        
    sessions = request.user.session_set.all()
    return render(request, 'user/manage_sessions.html', {'sessions': sessions})
