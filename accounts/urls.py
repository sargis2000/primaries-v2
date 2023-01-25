from django.urls import path, include

from primaries_app.views import GETStage

from .views import *


urlpatterns = [
    path("session/", SessionView.as_view(), name="session"),
    path("register/", UserApiView.as_view(), name="create_user"),
    path("csrf-cookie/", GetCSRFToken.as_view(), name="CSRF_token"),
    path("voter-profile/", VoterProfileAPIView.as_view(), name="voter_profile"),
    path(
        "resend-voter-profile-activation/",
        VoterProfileConfirmMail.as_view(),
        name="resend_voter_profile_activation",
    ),
    path(
        "activate-voter-profile/",
        ActivateVoterProfileAPIView.as_view(),
        name="activate_voter",
    ),
    path(
        "candidate-profile/",
        CandidateProfileAPIview.as_view(),
        name="candidate_profile",
    ),
    path(
        "resend-candidate-profile-activation/",
        CandidateProfileConfirmMail.as_view(),
        name="resend_candidate_activation",
    ),
    path(
        "activate-candidate-profile/",
        ActivateCandidateProfileAPIView.as_view(),
        name="activate_candidate",
    ),
    path(
        "candidate-post/", CandidatePostAPIView.as_view(), name="create_candidate_post"
    ),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("get-voter-profiles/", GetVoterProfiles.as_view(), name="get-voter-profiles"),
    path("get-stage/", GETStage.as_view(), name="get_stage"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("delete_user/", UserDeleteView.as_view(), name="delete_user"),
]
