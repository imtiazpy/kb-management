from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.contrib.auth.models import Group


from .models import User


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords didn't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data)['password1']

        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('name', 'avatar', 'password', 'is_active', 'is_superuser')


class UserAdmin(BaseUserAdmin):
    """
    This is a class that defines the admin interface for the CustomUser model. It sets the add_form, change_form, list_display, list_filter, fieldsets, add_fieldsets, search_fields, ordering, and filter_horizontal attributes to customize the admin interface. The add_fieldsets attribute defines the fields to be displayed when adding a new user. The class inherits from BaseUserAdmin.
    """

    add_form = UserCreationForm
    change_form = UserChangeForm

    list_display = ('id', 'name', 'is_active', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser', 'is_staff', 'is_active')

    fieldsets = (
        ('User Info', {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'avatar')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )

    add_fieldsets = (
        ('Custom User', {
            'classes': ('wide', ),
            'fields': ('username', 'name', 'password1', 'password2'),
        }),
    )

    search_fields = ('name', )
    filter_horizontal = ()




admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
