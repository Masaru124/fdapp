from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    """Home page view"""
    return render(request, 'index.html')

def about(request):
    """About page view"""
    return render(request, 'about.html')

@login_required
def dashboard(request):
    """User dashboard view"""
    context = {
        'user': request.user,
        # Add any additional context data needed for the dashboard
    }
    return render(request, 'user/dashboard.html', context)
