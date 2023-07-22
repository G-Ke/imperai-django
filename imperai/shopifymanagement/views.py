from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.forms import URLField


def handle_shopify_login_domain_search(request):
    url_field = URLField()
    if request.method == 'POST':
        shop = request.POST.get('shop')
        if not shop:
            messages.error(request, 'Shop domain is missing')
            return reverse('account_login')
        try:
            stripped_url = shop.strip('https://').strip('http://')
            url = url_field.clean(stripped_url)
        except ValidationError as e:
            messages.error(request, 'Invalid Shopify domain: ' + str(e.messages[0]))
            return redirect('account_login')
        bare_validated_url = str(url.strip('https://').strip('http://'))
        shopify_login_path = reverse('shopify_login') + '?shop=' + bare_validated_url
        full_shopify_login_url = 'http://127.0.0.1:8000' + shopify_login_path
        return redirect(full_shopify_login_url)
    return reverse('account_login')

def shopify_login_url_manager(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    else:
        shop = request.GET.get('shop')
        return redirect(f'/accounts/shopify/login?shop={shop}')