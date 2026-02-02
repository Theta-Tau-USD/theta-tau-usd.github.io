from django.shortcuts import render


def recruitment_landing(request):
    """Recruitment landing page."""
    return render(request, 'recruitment/landing.html')
