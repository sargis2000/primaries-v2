from django.contrib import admin

from .models import Pay


# Register your models here.


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    readonly_fields = (
        "EDP_BILL_NO",
        "EDP_AMOUNT",
        "EDP_REC_ACCOUNT",
        "confirmed",
        "profile",
    )

    def has_add_permission(self, request):
        """
        If the user is a superuser, then they can add a new object. Otherwise, they can't.

        :param request: The request object
        :return: The has_add_permission method is being returned.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        If the user is a superuser, they can delete the object. Otherwise, they can't

        :param request: The request object
        :param obj: The object being edited
        :return: The has_delete_permission method is being returned.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        "If the user is a superuser, then they have permission to change the object. Otherwise, they don't."

        The first line of the function is a conditional statement. If the user is a superuser, then the function returns
        True. Otherwise, the function returns False

        :param request: The request object
        :param obj: The object being edited
        :return: The has_change_permission method is being returned.
        """
        return False

    list_display = (
        "EDP_BILL_NO",
        "EDP_AMOUNT",
        "EDP_REC_ACCOUNT",
        "confirmed",
        "profile",
    )
