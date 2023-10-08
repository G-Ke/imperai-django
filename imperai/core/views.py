from typing import Any, Dict
from django.db import models
from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, CustomUser
from django.urls import reverse

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








"""    def get_success_url(self):
        is_htmx = self.request.headers.get('HX-Request')
        if is_htmx == 'true':
            print("hello")
            self.success_url = 'profile_user_name_swap.html'
            return self.success_url
        else:
            self.success_url = '/profile'
    """
"""    def form_valid(self, request, form):
        is_htmx = self.request.headers.get('HX-Request')
        if is_htmx == 'true':
            self.success_url = 'profile_user_name_swap.html'
            if form.is_valid():
                form.save()
                return render(request, 'partials/profile_user_name_swap.html')"""
        
"""    def get_success_url(self):
        is_htmx = self.request.headers.get('HX-Request')
        if is_htmx == 'true':
            return 'profile_user_name_swap.html'
        else:
            return self.success_url"""

"""@login_required(login_url='accounts/login')
def custom_user_update_view(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk, email=request.user.email)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'partials/profile_user_name_swap.html')
            return redirect('profile')"""