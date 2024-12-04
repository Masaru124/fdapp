from django.urls import path
from .views import auth_views, profile_views, general_views

urlpatterns = [
    # General views
    path('', general_views.home, name='home'),
    path('about/', general_views.about, name='about'),
    path('dashboard/', general_views.dashboard, name='dashboard'),

    # Authentication views
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.user_login, name='user_login'),
    path('logout/', auth_views.user_logout, name='user_logout'),
    path('activate/<str:uidb64>/', auth_views.activate_account, name='activate_account'),
    path('forgot-password/', auth_views.forgot_password, name='forgot_password'),
    path('change-password/', auth_views.change_password, name='change_password'),

    # Profile management views
    path('profile/', profile_views.profile, name='profile'),
    path('profile/delete/', profile_views.delete_account, name='delete_account'),
    path('profile/sessions/', profile_views.manage_sessions, name='manage_sessions'),
]
