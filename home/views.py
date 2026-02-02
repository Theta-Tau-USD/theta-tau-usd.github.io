from django.shortcuts import render


def home(request):
    """Home page with Theta Tau information."""
    return render(request, 'home/home.html')
