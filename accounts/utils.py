import requests
from django.conf import settings
from rest_framework import permissions
from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CandidatePermission(permissions.BasePermission):
    """class which check candidate permission"""

    def has_permission(self, request, view) -> bool:
        """
        If the request is a safe method (GET, HEAD, OPTIONS) or the user is a candidate, then return True

        :param request: The incoming request
        :param view: The view that the permission is being checked against
        :return: True or False
        """
        if request.method in permissions.SAFE_METHODS or request.user.is_candidate:
            return True


class VoterPermission(permissions.BasePermission):
    """class which check voter permission"""

    def has_permission(self, request, view) -> bool:
        """
        If the request is a safe method (GET, HEAD, OPTIONS) or the user is a voter, then return True

        :param request: The request object
        :param view: The view that the permission is being checked against
        :return: True or False
        """
        if request.method in permissions.SAFE_METHODS or request.user.is_voter:
            return True


def custom_exception_handler(exc, context):
    """
    It takes the response from the default exception handler and replaces the detail key with a custom message

    :param exc: The exception instance raised
    :param context: The context variable contains a Request object, which is the initial request that triggered the
    exception
    :return: Հարցումն ընդհատվել է : Հասանելի կլինի {time} վայրկյանից:
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):  # check that a Throttled exception is raised
        time = response.data["detail"].split()[6]
        response.data[
            "detail"
        ] = f"Հարցումն ընդհատվել է : Հասանելի կլինի {time} վայրկյանից:"

    return response


def send_mailgun_mail(
    form: str, to: list, subject: str | None, message: str
) -> Response:
    """
    It sends an email using the Mailgun API

    :param form: The email address that the email is sent from
    :type form: str
    :param to: list of email addresses to send to
    :type to: list
    :param subject: The subject of the email
    :type subject: str | None
    :param message: The message you want to send
    :type message: str
    :return: A response object.
    """
    result = requests.post(
        "https://api.mailgun.net/v3/primaries.am/messages",
        auth=("api", settings.EMAIL_HOST_PASSWORD),
        data={"from": form, "to": to, "subject": subject, "text": message},
    )
    return result
