import requests
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Sum
from rest_framework import permissions, status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from accounts.models import CandidatePost, CandidateProfile, VoterProfile
from accounts.serializers import CandidatePostSerializer, CandidateProfileSerializer
from accounts.utils import VoterPermission, send_mailgun_mail
from .models import (
    EvaluateModel,
    GlobalConfigs,
    MarkModel,
    News,
    VotingModel,
    choice_stage,
)
from .serializers import *


__all__ = [
    "MarkCandidateAPIView",
    "EvaluateAPIView",
    "NewsAPIView",
    "GetCandidateProfiles",
    "GetCandidateByID",
    "SendMailAPIVIEW",
    "GetEvaluateResult",
    "VoteView",
    "GETStage",
    "VoteResult",
    "PayViaImageApiView",
    "Party"
]


def has_dublicates(votes: list) -> bool:
    """
    It returns True if there are any duplicates in the list, and False otherwise

    :param votes: list
    :type votes: list
    :return: True or False
    """

    for i in votes:
        if votes.count(i) > 1:
            return True
    return False


def valid_ids(votes: list) -> bool:
    """
    It checks if the list of candidate ids in the votes are valid

    :param votes: list of candidate ids
    :type votes: list
    :return: A list of candidate ids
    """
    candidate_ids = [str(i.id) for i in CandidateProfile.objects.all()]
    for id in votes:
        if id not in candidate_ids:
            return False
    return True


class MarkCandidateAPIView(APIView):
    """This class is a subclass of the APIView class, and it's purpose is to mark a candidate as hired."""

    permission_classes = [permissions.IsAuthenticated, VoterPermission]

    def get(self, request) -> Response:
        """
        It takes a request, gets all the MarkModel objects, serializes them, and returns them in a response

        :param request: The request object
        :return: A list of all the marks in the database.
        """

        choice_queryset = MarkModel.objects.all().order_by("mark")
        serializer = MarkModelSerializer(instance=choice_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EvaluateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, VoterPermission]

    def get(self, request):
        """
        If the user has voted for the candidate, return the model, otherwise return False

        :param request: The request object
        :return: The serializer.data is being returned.
        """
        candidate_id = request.query_params.get("candidate", None)
        if candidate_id:
            try:
                voter_profile = VoterProfile.objects.get(user_id=request.user.id)
                try:
                    result = EvaluateModel.objects.get(
                        voter_id=voter_profile.id, candidate_id=candidate_id
                    )
                except EvaluateModel.DoesNotExist:
                    result = None
                serializer = EvaluateModelSerializer(instance=result)
            except VoterProfile.DoesNotExist:
                raise ValidationError(
                    "Ընտրողի Սխալ. էջը գոյություն չունի!, Նախ ստեղծեք  Ընտրողի էջ․"
                )

            if result:
                # if serializer.is_valid():
                return Response(
                    {"voted": True, "model": serializer.data}, status=status.HTTP_200_OK
                )
                # return Response({'voted': True, 'model': serializer.errors}, status=status.HTTP_200_OK)
            return Response({"voted": False}, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Թեկնածուի ID-ն բացակայում է")

    def post(self, request) -> Response:
        """
        The function takes a request object, and returns a response object

        :param request: The request object
        :return: The serializer.data is being returned.
        """
        try:
            request.data["voter"] = VoterProfile.objects.get(user_id=request.user.id).id
        except VoterProfile.DoesNotExist:
            raise ValidationError(
                "Ընտրողի Սխալ. էջը գոյություն չունի!, Նախ ստեղծեք  Ընտրողի էջ․"
            )

        try:
            exist = EvaluateModel.objects.filter(
                voter_id=request.data["voter"], candidate_id=request.data["candidate"]
            ).first()
        except EvaluateModel.DoesNotExist:
            exist = None
        if exist:
            exist.poll = MarkModel.objects.get(id=request.data["poll"])
            exist.save()
            serializer = EvaluateModelSerializer(data=request.data, instance=exist)
            if serializer.is_valid():
                return Response(
                    {"data_updated": serializer.data}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_200_OK)
        serializer = EvaluateModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsAPIView(APIView):
    """Class which returns news objects in order by creation date"""

    def get(self, request):
        """
        It gets the id from the query params, if it exists, and if it does, it tries to get the news by id, and if it
        doesn't exist, it returns a response saying that the news does not exist, and if it does exist, it returns the
        serialized data

        :param request: The request object is the first parameter to any view. It contains all the information about the
        request that was made to the server
        :return: A list of all the news objects in the database.
        """
        id = request.query_params.get("id", None)
        if id is not None:
            try:
                news_by_id = News.objects.get(id=id)
            except News.DoesNotExist:
                return Response(
                    "New does not exist", status=status.HTTP_400_BAD_REQUEST
                )
            else:
                serializer = NewsSerializer(instance=news_by_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
        news = News.objects.all().order_by("created_at")
        serializer = NewsSerializer(instance=news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCandidateProfiles(APIView):
    def get(self, request) -> Response:
        """
        It returns a list of all candidate profiles

        :param request: The request object
        :return: A list of all the candidate profiles.
        """
        response = CandidateProfile.objects.filter(user__is_candidate=True)
        serializer = CandidateProfilesSerializer(instance=response, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCandidateByID(APIView):
    permission_classes = (IsAuthenticated, VoterPermission)

    def get(self, request):
        """
        It gets a candidate profile and then gets all the posts associated with that profile and returns them in a response

        :param request: The request object
        :return: The candidate profile and the candidate posts
        """
        try:
            candidate = CandidateProfile.objects.get(
                id=request.query_params.get("id", None)
            )
        except CandidateProfile.DoesNotExist:
            return Response(
                "Candidate profile does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        else:
            posts = CandidatePost.objects.filter(profile=candidate)
            post_serializer = CandidatePostSerializer(instance=posts, many=True)
            serializer = CandidateProfileSerializer(instance=candidate)
            return Response(
                {"profile": serializer.data, "posts": post_serializer.data},
                status=status.HTTP_200_OK,
            )


class SendMailAPIVIEW(APIView):
    """This class is a subclass of the APIView class, and it's purpose is to send an email to the user."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        It takes a request, gets the data from the request, gets the candidate profile from the database, sends an email to
        the candidate, and returns a response

        :param request: The request object
        :return: The response is a string.
        """
        data = self.request.data
        full_name = data["full_name"]
        from_mail = data["email"]
        message = data["message"]
        admin = data.get("admin", None)
        try:
            candidate = CandidateProfile.objects.get(id=data["candidate_id"])
            to_mail = candidate.user.email
            if admin is not None:
                to_mail = settings.ADMIN_EMAIL
        except CandidateProfile.DoesNotExist:
            return Response(
                "Candidate profile does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        else:
            message += f"\n\nՀարգանքներով {full_name}"
            res = send_mailgun_mail(
                form=from_mail, to=to_mail, subject=None, message=message
            )

            if res.status_code != 200:
                return Response(f"email not sent.", status=status.HTTP_400_BAD_REQUEST)
            return Response(f"email sent successful", status=status.HTTP_200_OK)


class GetEvaluateResult(APIView):
    def get(self, request):
        """
        It takes a candidate ID as a query parameter, and if it exists, it returns the sum of the points of all the polls
        that the candidate has participated in.

        If the candidate ID is not provided, it returns the sum of the points of all the polls that all the candidates have
        participated in

        :param request: The request object
        :return: The sum of the points of the candidate.
        """
        candidate_id = request.query_params.get("candidate", None)
        if GlobalConfigs.objects.get(id=1).stage != "2":
            return Response(
                "Այս փուլում գնահատման արդյունքները հասանելի չեն",
                status=status.HTTP_409_CONFLICT,
            )
        if candidate_id:
            try:
                candidate_profile = CandidateProfile.objects.get(id=candidate_id)
            except CandidateProfile.DoesNotExist:
                return Response(
                    "Նշված ID-ով Թեկնածու գոյություն չունի",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                if not candidate_profile.user.is_candidate:
                    return Response(
                        "Նշված ID-ով Թեկնածուն հասանելի չէ",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                queryset = EvaluateModel.objects.filter(candidate=candidate_profile)
                res = sum([i.poll.mark for i in queryset])
                return Response({"points": res})

        else:
            res = (
                EvaluateModel.objects.values("candidate")
                .order_by("candidate")
                .annotate(points=Sum("poll__mark"))
            )
            return Response(res, status.HTTP_200_OK)


class VoteView(APIView):
    permission_classes = (permissions.IsAuthenticated, VoterPermission)

    def post(self, request):
        """
        It takes a list of candidate ids, checks if the voter has already voted, if not, it creates a voting model for each
        candidate id in the list

        :param request: The request object
        """
        # Getting the votes from the request.data and then getting the stage from the
        # GlobalConfigs.objects.get(id=1).stage
        votes = request.data.get("votes", None)
        stage = GlobalConfigs.objects.get(id=1).stage
        try:
            voter_profile = VoterProfile.objects.get(user=request.user)
        except VoterProfile.DoesNotExist:
            return Response("Ընտրողի տվյալների սխալ")

        if votes is None:
            return Response(
                "ընտրության տվյալները դատարկ են", status=status.HTTP_400_BAD_REQUEST
            )

        # Checking if the stage is 5 and if the length of the votes is not 7.
        if GlobalConfigs.objects.get(id=1).stage == "5":
            if len(votes) != 7:
                return Response(
                    "Պետք է ընտրել Ճիշտ 7 թեկնածու", status=status.HTTP_400_BAD_REQUEST
                )
        else:

            # The above code is checking if the length of the votes is less than 10.
            if len(votes) < 10:
                return Response(
                    "Պետք է ընտրել արնվազն 10  թեկնածու",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Checking if there are any dublicates in the votes list.
            if has_dublicates(votes):
                return Response("Սխալ քվեաթերթիկ", status=status.HTTP_400_BAD_REQUEST)
            # Checking if the votes are valid.
            if not valid_ids(votes):
                return Response(
                    "Թեկնածուների ID-ների Սխալ", status=status.HTTP_400_BAD_REQUEST
                )

            # Checking if the voter has already voted in the current stage.
            if VotingModel.objects.filter(voter=voter_profile, stage=stage).exists():
                return Response(
                    "Ընտրողը արդեն քվերկել է", status=status.HTTP_400_BAD_REQUEST
                )

            # Checking if the number of male and female candidates is less than 27%
            candidates = CandidateProfile.objects.filter(id__in=votes).values_list(
                "gender"
            )
            if (
                len([i[0] for i in candidates if i[0] == "male"])
                / len(candidates)
                * 100
                < 27
            ):
                return Response(
                    "Արական թեկնածուների քանակը պետք է գեռազանցի 27% ը",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if (
                len([i[0] for i in candidates if i[0] == "female"])
                / len(candidates)
                * 100
                < 27
            ):
                return Response(
                    "Իգական թեկնածուների քանակը պետք է գեռազանցի 27% ը",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # The above code is enumerating the votes list and assigning the index to i and the value to j.
        for i, j in enumerate(votes, start=1):
            # Checking if the value of i is greater than the number of CandidateProfile objects in the database.
            if i > CandidateProfile.objects.all().count():
                return Response(
                    "Ընտրության համարի սԽալ", status=status.HTTP_400_BAD_REQUEST
                )
            # Creating a voting model object.
            try:
                VotingModel.objects.create(
                    voter=voter_profile,
                    candidate=CandidateProfile.objects.get(id=j),
                    position=i,
                    points=1 / i * voter_profile.votes_count,
                    stage=stage,
                )
            except CandidateProfile.DoesNotExist:
                return Response(
                    f"Նշված ID ով թեկնածու գոյություն չունի id={j}",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            voter_profile.already_voted = True
            voter_profile.save()
        return Response("OK", status.HTTP_200_OK)


class GETStage(APIView):
    def get(self, request):
        """
        It returns a response with the stage of the GlobalConfigs object with id=1

        :param request: The request object
        :return: The stage of the game.
        """
        stage = GlobalConfigs.objects.get(id=1).stage
        name = None
        for i in choice_stage:
            if i[0] == stage:
                name = i[1]
                break

        return Response({"stage": stage, "name": name}, status=status.HTTP_200_OK)


def get_vote_result(stage: int, id: str):
    if id is not None:
        res = {
            id: VotingModel.objects.filter(candidate_id=id, stage=stage).values_list(
                "points"
            )
        }
    else:
        res = (
            VotingModel.objects.filter(stage=stage)
            .values_list("candidate")
            .order_by("candidate")
            .annotate(points=Sum("points"))
        )
    return res


class VoteResult(APIView):
    def get(self, request):
        stage = GlobalConfigs.objects.get(id=1).stage
        # Ստուգում է արդյունքները անհասնելի են թե ոչ
        if stage not in ("4", None):
            return Response(
                "Այս փուլում ընտրության արդյունքները անհասնելի են",
                status=status.HTTP_409_CONFLICT,
            )
        id = request.query_params.get("id", None)
        if stage == "4":
            res = get_vote_result(stage=3, id=id)
        else:
            res = get_vote_result(stage=5, id=id)
        return Response(res, status=status.HTTP_200_OK)


class PayViaImageApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            voter_profile = request.user.voterprofile
        except VoterProfile.DoesNotExist:
            return Response(
                "Օգտագործողը ընտրողի էջ չունի", status=status.HTTP_400_BAD_REQUEST
            )
        else:
            request.data["voter_profile"] = voter_profile.pk
        serializer = PayViaImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Party(APIView):

    def get(self, requset):
        values = CandidateProfile.objects.all().values_list('party', flat=True)
        values = set(values)
        print(values)
        return Response({"party": values}, status=status.HTTP_200_OK)