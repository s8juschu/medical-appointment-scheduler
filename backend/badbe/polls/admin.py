from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from polls.models import Employee, Department, Account, Template
from polls.models import Employee, Department, Account, Appointment

# Django's built-in UserCreationForm and UserChangeForm are tied to User and need to be
# rewritten or extended to work with a custom user model


class AccountCreationForm(UserCreationForm):
    """
    A form for creating new Accounts.
    """

    class Meta(forms.ModelForm):
        model = Account
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name',)

    def clean_password2(self):
        # Check that the two password entries match
        # TODO: implement full password check
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not (password1 and password2 and password1 == password2):
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountChangeForm(UserChangeForm):
    """
    A form for updating Accounts.
    """

    password = ReadOnlyPasswordHashField()

    class Meta(forms.ModelForm):
        model = Account
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


# Register the models which should be managed by the admin module
admin.site.register(Account, UserAdmin)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Template)
admin.site.register(Appointment)
