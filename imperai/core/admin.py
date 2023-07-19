from django.contrib import admin
from .models import CustomUser, Profile
# Register your models here.

admin.site.site_header = "imperai Backend"
admin.site.site_title = "imperai Backend Portal"
admin.site.index_title = "Welcome to imperai Backend Portal"

class CustomUserAdmin(admin.ModelAdmin):
    fields = ['email', 'password', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions']

admin.site.register(CustomUser, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'location', 'title']

admin.site.register(Profile, ProfileAdmin)