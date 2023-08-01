import uuid
from django.db import models

# Create your models here.


class ShopifyStore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store_manager = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE)
    staff = models.ManyToManyField('core.CustomUser', related_name='staff')
    is_active = models.BooleanField(default=True)
    shopify_id = models.CharField(max_length=255, unique=True)
    shopify_name = models.CharField(max_length=255, unique=True)
    domain = models.CharField(max_length=255, unique=True)
    province = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    primary_locale = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    country_code = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)
    money_format = models.CharField(max_length=255)
    province_code = models.CharField(max_length=255)
    taxes_included = models.BooleanField()
    myshopify_domain = models.CharField(max_length=255)
    eligible_for_payments = models.BooleanField()
    has_storefront = models.BooleanField()
    enabled_presentment_currencies = models.CharField(max_length=255)
    shopify_associated_user = models.JSONField()

    def __str__(self):
        return self.shopify_name