from django.urls import path
from . import views

urlpatterns = [
    path('request-task/', views.request_task, name='request_task'),
    path('track-progress/', views.track_progress, name='track_progress'),
]