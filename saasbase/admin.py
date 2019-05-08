from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

#from awl.admintools import make_admin_obj_mixin
from awl.utils import get_field_names

from saasbase.models import Login, Account #, AccountAddress
from saasbase.contacts import PersonalInfo, PhoneInfo, BirthDayInfo

# =============================================================================
# Remove Modules From Admin

admin.site.unregister(Group)

# ============================================================================
# Logins: Custom User Model

info_fields = tuple(get_field_names(PersonalInfo, exclude=['email',])) + \
    tuple(get_field_names(PhoneInfo)) + tuple(get_field_names(BirthDayInfo))

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', strip=False,
        widget=forms.PasswordInput, 
        help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password confirmation', strip=False,
        widget=forms.PasswordInput,
        help_text='Enter same password for verification')

    class Meta:
        model = Login
        fields = ('email', )

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match")
        return p2

    def _post_clean(self):
        super()._post_clean()

        # validate password 
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password1', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='<a href="{}">Change password</a>')

    class Meta:
        model = Login
        fields = ('email', 'password', 'is_active', 'is_admin') + info_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = \
            self.fields['password'].help_text.format('../password/')

    def clean_password(self):
        return self.initial['password']


@admin.register(Login)
class LoginAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'first_name', 'last_name', 'is_admin', 
        'is_active')
    list_filter = ('is_admin', )

    readonly_fields = ('created', 'last_login', )

    fieldsets = (
        (None, {'fields':('email', 'password')}),
        ('Personal Info', {'fields':info_fields}),
        ('Important Dates', {'fields': ('last_login', 'created')}),
    )

    add_fieldsets = (
        (None, {
            'classes':('wide', ),
            'fields':('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()


# ============================================================================
# Account 

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', )


#base = make_admin_obj_mixin('AccountAddressMixin')
#base.add_obj_link('show_account', 'account')
#
#@admin.register(AccountAddress)
#class AccountAddressAdmin(admin.ModelAdmin, base):
#    list_display = ('name', 'show_account', 'address1', 'city')
#    list_filter = ('account', )
