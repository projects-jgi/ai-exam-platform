from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('auth/register/', views.user_registration_view, name='user-register'),
    path('auth/login/', views.user_login_view, name='user-login'),
    path('auth/logout/', views.user_logout_view, name='user-logout'),
    
    # Profile URLs
    path('profile/me/', views.current_user_profile_view, name='current-user-profile'),
]