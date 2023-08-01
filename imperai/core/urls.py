from django.contrib import admin
from django.urls import path, include
from .views import DashboardView, ProfileView, ProfileUpdateView, CustomUserUpdateView

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/user/update/<int:pk>', CustomUserUpdateView.as_view(), name='user_update'),
]