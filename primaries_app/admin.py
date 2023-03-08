from django import forms
from django.contrib import admin
from django.utils.html import strip_tags

from .models import (
    EvaluateModel,
    GlobalConfigs,
    MarkModel,
    News,
    VotingModel,
    PayViaImage,
)


@admin.register(GlobalConfigs)
class ConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MarkModel)
class MarkAdmin(admin.ModelAdmin):
    """Mark model admin"""

    @staticmethod
    def text(obj):
        return strip_tags(obj.content)[:30] + "..."

    list_display = (
        "text",
        "mark",
    )
    search_fields = ("mark",)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "content":
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


@admin.register(EvaluateModel)
class PollingAdmin(admin.ModelAdmin):
    """Evaluate model admin"""

    list_display = (
        "voter",
        "candidate",
    )
    list_filter = (
        "voter",
        "candidate",
    )
    search_fields = (
        "voter",
        "candidate",
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)


@admin.register(VotingModel)
class VotingAdmin(admin.ModelAdmin):
    list_display = ("voter", "candidate", "position", "stage", "points")
    list_filter = ("voter", "candidate", "position", "stage", "points")
    ordering = ("voter", "position")


@admin.register(PayViaImage)
class PayViaImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_voter_profile_full_name",
        "get_picture",
    )
    search_fields = ("voter_profile__first_name", "voter_profile__last_name", "id")
