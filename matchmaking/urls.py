from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # Matchmaking section
    path('matchmaking/', views.landing_page, name='matchmaking_landing'),
    path('matchmaking/login/', views.user_login, name='login'),
    path('matchmaking/logout/', views.user_logout, name='logout'),
    path('matchmaking/dashboard/', views.dashboard, name='dashboard'),
    
    # Admin URLs
    path('matchmaking/admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('matchmaking/admin-dashboard/create-user/', views.admin_create_user, name='admin_create_user'),
    
    # Brother URLs
    path('matchmaking/brother/profile/create/', views.brother_profile_create, name='brother_profile_create'),
    path('matchmaking/brother/success/', views.brother_success, name='brother_success'),
    
    # PNM URLs
    path('matchmaking/pnm/profile/create/', views.pnm_profile_create, name='pnm_profile_create'),
    path('matchmaking/pnm/results/', views.pnm_results, name='pnm_results'),
]
