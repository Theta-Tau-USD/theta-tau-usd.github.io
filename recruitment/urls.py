from django.urls import path
from . import views

urlpatterns = [
    path('recruitment/', views.recruitment_landing, name='recruitment'),
]
