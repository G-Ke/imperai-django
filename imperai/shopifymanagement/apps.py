from django.apps import AppConfig


class ShopifyManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopifymanagement'

    class Meta:
        app_label = 'shopifymanagement'