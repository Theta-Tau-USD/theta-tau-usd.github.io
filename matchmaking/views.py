from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.db import connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib.parse
from .models import CustomUser, BrotherProfile, PNMProfile
from .forms import (
    AdminCreateUserForm, 
    BrotherProfileForm, 
    PNMProfileForm,
    CustomLoginForm
)


def health_check(request):
    """Health check endpoint for Railway monitoring"""
    try:
        # Check database connectivity
        connection.ensure_connection()
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)


def landing_page(request):
    """Landing page with sign-in options for matchmaking"""
    return render(request, 'matchmaking/landing.html')


def user_login(request):
    """Login view for all user types"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomLoginForm()
    
    return render(request, 'matchmaking/login.html', {'form': form})


def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """
    Dashboard view that redirects based on user role
    """
    user = request.user
    
    if user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif user.role == 'BROTHER':
        # Check if brother has a profile
        if hasattr(user, 'brother_profile'):
            return redirect('brother_success')
        else:
            return redirect('brother_profile_create')
    elif user.role == 'PNM':
        # Check if PNM has a profile
        if hasattr(user, 'pnm_profile'):
            return redirect('pnm_results')
        else:
            return redirect('pnm_profile_create')
    
    return redirect('matchmaking_landing')


# ADMIN VIEWS
@login_required
def admin_dashboard(request):
    """Admin dashboard for creating accounts"""
    if request.user.role != 'ADMIN':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
    
    brothers = BrotherProfile.objects.all()
    pnms = PNMProfile.objects.all()
    
    context = {
        'brothers': brothers,
        'pnms': pnms,
    }
    return render(request, 'matchmaking/admin_dashboard.html', context)


@login_required
def admin_create_user(request):
    """Admin view to create Brother or PNM accounts"""
    if request.user.role != 'ADMIN':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            
            # Generate username from email
            username = email.split('@')[0]
            
            # Generate random password
            password = get_random_string(12)
            
            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role
            )
            
            messages.success(
                request, 
                f'Account created successfully! Username: {username} | Password: {password}'
            )
            return redirect('admin_dashboard')
    else:
        form = AdminCreateUserForm()
    
    return render(request, 'matchmaking/admin_create_user.html', {'form': form})


# BROTHER VIEWS
@login_required
def brother_profile_create(request):
    """Brother profile creation view"""
    if request.user.role != 'BROTHER':
        messages.error(request, 'Access denied. Brothers only.')
        return redirect('dashboard')
    
    # Check if profile already exists
    if hasattr(request.user, 'brother_profile'):
        return redirect('brother_success')
    
    if request.method == 'POST':
        form = BrotherProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('brother_success')
    else:
        form = BrotherProfileForm()
    
    return render(request, 'matchmaking/brother_profile_form.html', {'form': form})


@login_required
def brother_success(request):
    """Success page for brothers after profile creation"""
    if request.user.role != 'BROTHER':
        messages.error(request, 'Access denied. Brothers only.')
        return redirect('dashboard')
    
    if not hasattr(request.user, 'brother_profile'):
        return redirect('brother_profile_create')
    
    profile = request.user.brother_profile
    return render(request, 'matchmaking/brother_success.html', {'profile': profile})


# PNM VIEWS
@login_required
def pnm_profile_create(request):
    """PNM profile creation view"""
    if request.user.role != 'PNM':
        messages.error(request, 'Access denied. PNMs only.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PNMProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('pnm_results')
    else:
        form = PNMProfileForm()
    
    return render(request, 'matchmaking/pnm_profile_form.html', {'form': form})


@login_required
def pnm_results(request):
    """Display matched brothers for PNM"""
    if request.user.role != 'PNM':
        messages.error(request, 'Access denied. PNMs only.')
        return redirect('dashboard')
    
    if not hasattr(request.user, 'pnm_profile'):
        return redirect('pnm_profile_create')
    
    pnm_profile = request.user.pnm_profile
    
    # Get all brother profiles
    brothers = BrotherProfile.objects.all()
    
    if brothers.count() == 0:
        messages.info(request, 'No brothers available yet. Check back later!')
        return render(request, 'matchmaking/pnm_results.html', {'matches': []})
    
    # Perform matching using TF-IDF and cosine similarity
    matches = find_matching_brothers(pnm_profile, brothers)
    
    return render(request, 'matchmaking/pnm_results.html', {
        'pnm_profile': pnm_profile,
        'matches': matches
    })


def find_matching_brothers(pnm_profile, brothers):
    """
    Find the top 3 matching brothers using TF-IDF and cosine similarity
    """
    if brothers.count() == 0:
        return []
    
    # Prepare descriptions
    brother_descriptions = [b.description for b in brothers]
    pnm_description = pnm_profile.description
    
    # Combine all descriptions
    all_descriptions = brother_descriptions + [pnm_description]
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
    tfidf_matrix = vectorizer.fit_transform(all_descriptions)
    
    # Get PNM vector (last one)
    pnm_vector = tfidf_matrix[-1]
    
    # Get brother vectors (all except last)
    brother_vectors = tfidf_matrix[:-1]
    
    # Calculate cosine similarity
    similarities = cosine_similarity(pnm_vector, brother_vectors).flatten()
    
    # Create list of (brother, similarity_score) tuples
    brother_scores = list(zip(brothers, similarities))
    
    # Sort by similarity score (descending)
    brother_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Get top 3 matches
    top_matches = brother_scores[:3]
    
    # Format results with similarity percentage
    matches = []
    for brother, score in top_matches:
        matches.append({
            'brother': brother,
            'match_percentage': round(score * 100, 1),
            'calendar_link': generate_calendar_link(pnm_profile, brother)
        })
    
    return matches


def generate_calendar_link(pnm_profile, brother):
    """
    Generate a Google Calendar link for scheduling a coffee chat
    """
    event_title = f"Coffee Chat: {pnm_profile.name} & {brother.name}"
    event_details = f"Coffee chat between {pnm_profile.name} (PNM) and {brother.name} (Brother)\n\nDiscuss interests, Theta Tau, and get to know each other!"
    
    # URL encode parameters
    params = {
        'action': 'TEMPLATE',
        'text': event_title,
        'details': event_details,
        'add': f"{pnm_profile.user.email},{brother.user.email}",
    }
    
    base_url = 'https://calendar.google.com/calendar/render'
    query_string = urllib.parse.urlencode(params)
    
    return f"{base_url}?{query_string}"
