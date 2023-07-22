from django.contrib import admin
from django.urls import path, include
from .views import handle_shopify_login_domain_search, shopify_login_url_manager

urlpatterns = [
    path('shopifyDomainSearch', handle_shopify_login_domain_search, name='shopify_domain_search'),
    path('shopifyLoginUrlManager', shopify_login_url_manager, name='shopify_login_url_manager')
]