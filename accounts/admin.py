from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount
from django import forms
from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django_rest_passwordreset.models import ResetPasswordToken
from django.template.response import TemplateResponse
from django.urls import path
from rest_framework.authtoken.models import TokenProxy

from .models import CandidatePost, CandidateProfile, User, VoterProfile
from .views import send_email_view


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. All the required
    fields are plus repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        """
        If the two passwords don't match, raise a validation error
        :return: The password2 is being returned.
        """
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """
        The function takes the password from the form, hashes it, and saves it to the database

        :param commit: A boolean that tells Django whether to save the User object after the form is validated, defaults to
        True (optional)
        :return: The user object is being returned.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def make_inactive(self, request, queryset):
        """
        It takes a queryset of objects, and sets the is_active field to False

        :param request: The current request
        :param queryset: The queryset of objects to be acted upon
        """
        queryset.update(is_active=False)

    make_inactive.short_description = "Ապակտիվացնել նշված օգտատերերին"

    def make_active(self, request, queryset):
        """
        It takes a queryset of objects, and updates the is_active field to True

        :param request: The current request
        :param queryset: The queryset of objects to be acted upon
        """
        queryset.update(is_active=True)

    make_active.short_description = "Ակտիվացնել նշված օգտատերերին"

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Statuses",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "is_voter",
                    "is_candidate",
                )
            },
        ),
        (None, {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    list_filter = ("is_voter", "is_candidate", "is_active")
    list_display = ("email", "is_voter", "is_candidate", "is_active")
    readonly_fields = ("date_joined", "is_candidate", "is_voter")
    actions = (
        "make_inactive",
        "make_active",
        "delete_selected",
    )
    ordering = ("date_joined",)


@admin.register(CandidatePost)
class PostAdmin(admin.ModelAdmin):
    model = CandidatePost
    list_display = ("get_user", "title")
    list_filter = ("profile",)
    search_fields = ("title",)

    @display(ordering="profile__user", description="user")
    def get_user(self, obj):
        """
        The function takes in an object (obj) and returns the email of the user who created the object

        :param obj: The object that is being serialized
        :return: The email of the user who created the post.
        """
        user = obj.profile.user
        return user.email


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    def send_mail_action(self, request, queryset):
        """
        It takes a queryset of objects, and sends an email to each object's email address

        :param request: The request object
        :param queryset: The queryset of objects that are selected
        """

        return TemplateResponse(
            request,
            "send_mail.html",
            context={"emails": queryset.values_list("user__email", flat=True)},
        )

    send_mail_action.short_description = "Ուղղարկել նամակ Նշված  թեկնածուներին"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "send_email_view/",
                self.admin_site.admin_view(send_email_view, cacheable=True),
                name="send_mail_splash",
            ),
        ]
        return my_urls + urls

    @staticmethod
    def full_name(obj):
        """
        It returns a string that is the email of the user associated with the profile, followed by the string " profile"

        :param obj: The object that the model is attached to
        :return: The full name of the user.
        """
        return "{0} profile".format(obj.user.email)

    list_display = (
        "first_name",
        "last_name",
        "gender",
        "phone_number",
        "get_picture",
        "is_approved",
    )
    list_filter = ("gender", "party", "is_approved")
    search_fields = (
        "phone_number",
        "first_name",
        "last_name",
        "party",
    )
    actions = ("send_mail_action", "delete_selected")


@admin.register(VoterProfile)
class VoterProfile(admin.ModelAdmin):
    def send_mail_action(self, request, queryset):
        """
        It takes a queryset of objects, and sends an email to each object's email address

        :param request: The request object
        :param queryset: The queryset of objects that are selected
        """

        return TemplateResponse(
            request,
            "send_mail.html",
            context={"emails": queryset.values_list("email", flat=True)},
        )

    send_mail_action.short_description = "Ուղղարկել նամակ Նշված  ընտրողներին։"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "send_email_view/",
                self.admin_site.admin_view(send_email_view, cacheable=True),
                name="send_mail_splash",
            ),
        ]
        return my_urls + urls

    @staticmethod
    def full_name(obj):
        return "{0} profile".format(obj.user.email)

    list_display = (
        "first_name",
        "last_name",
        "phone_number",
        "address",
        "is_email_verified",
    )
    search_fields = ("phone_number", "first_name", "last_name")
    list_filter = (
        "is_email_verified",
        "is_paid",
    )


admin.site.unregister(ResetPasswordToken)
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(TokenProxy)
