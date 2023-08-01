from typing import Any, Dict
from django.db import models
from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, CustomUser

# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = 'accounts/login'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"
    login_url = 'accounts/login'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "profile_update.html"
    login_url = 'accounts/login'
    model = Profile
    success_url = '/profile'
    fields = ['location', 'title']

    def get_initial(self):
        initial =  super(ProfileUpdateView, self).get_initial()
        Profile.objects.get(user=self.request.user)
        return initial
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "user_update.html"
    login_url = 'accounts/login'
    model = CustomUser
    success_url = '/profile'
    fields = ['first_name', 'last_name']

    def get_initial(self):
        initial =  super(CustomUserUpdateView, self).get_initial()
        CustomUser.objects.get(email=self.request.user.email)
        return initial
    
    def get_queryset(self):
        return CustomUser.objects.filter(email=self.request.user.email)