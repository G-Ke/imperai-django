from django.contrib import admin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    fields = ['email', 'password', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions']

admin.site.register(CustomUser, CustomUserAdmin)