from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse


class MyAccountAdapter(DefaultSocialAccountAdapter):
    
    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            return reverse('welcome')
        else:
            return super().get_login_redirect_url(request)