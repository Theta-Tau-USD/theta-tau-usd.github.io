from django.urls import path
from . import views

urlpatterns = [
    path('exec-board/', views.exec_board, name='exec_board'),
]
