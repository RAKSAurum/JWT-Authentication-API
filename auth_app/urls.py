from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('verify/', views.verify_token, name='verify_token'),
    path('validate/', views.validate_token, name='validate_token'),
]