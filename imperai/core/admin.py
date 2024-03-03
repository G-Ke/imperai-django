from django.contrib import admin
from .models import CustomUser, Profile, TokenIdentifier
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
# Register your models here.

admin.site.site_header = "imperai Backend"
admin.site.site_title = "imperai Backend Portal"
admin.site.index_title = "Welcome to imperai Backend Portal"

""" class CustomUserAdmin(admin.ModelAdmin):
    fields = ['email', 'password', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', 'token_id']

admin.site.register(CustomUser, CustomUserAdmin) """


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'location', 'title']

admin.site.register(Profile, ProfileAdmin)


class TokenIdentifierAdmin(admin.ModelAdmin):
    fields = ['user', 'token_id']
    list_display = ['user', 'token_id']
    readonly_fields = ('user', 'token_id',)

admin.site.register(TokenIdentifier, TokenIdentifierAdmin)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'token_id')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'token_id', 'last_login', 'date_joined')

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'token_id']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    fieldsets = [
        (None, {'fields': ['email', 'password', 'first_name', 'last_name', 'last_login', 'date_joined']}),
        ('API', {'fields': ['token_id']}),
        ('Permissions', {"fields": ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions']}),
    ]
    add_fieldsets = [
        (
            None, 
            {
                'classes': ['wide'],
                'fields': ['email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'token_id']
            }
        )
    ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ['groups', 'user_permissions']

admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)