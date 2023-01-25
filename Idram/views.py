from hashlib import md5

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import VoterProfile

from .models import Pay
from .serializers import PaySerializer


values = {
    "1": "2.00",
    "2": "3.00",
    "3": "4.00",
    "4": "5.00",
    "5": "6.00",
}


class PayForEvaluate(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        If the user has a voter profile, and the user has not paid, then create a payment object and return it

        :param request: The request object
        :return: The data is being returned as a dictionary.
        """
        print(self.request.user)
        try:
            voter_profile = VoterProfile.objects.get(user_id=request.user.id)
        except VoterProfile.DoesNotExist:
            return Response("Օգտատերը ընտրողի էջ չունի", status.HTTP_400_BAD_REQUEST)
        else:
            if voter_profile.is_paid:
                return Response(
                    "Օգտատերը արդեն վճարել է գնահատման համար",
                    status.HTTP_400_BAD_REQUEST,
                )
            data = Pay.objects.get_or_create(profile=voter_profile, EDP_AMOUNT="1.00")
            serializer = PaySerializer(data[0])
            return Response(serializer.data, status=status.HTTP_200_OK)


class PayForVoting(APIView):
    def get(self, request):
        """
        It takes a request, checks if the request has a query parameter called count, if it doesn't it returns a response
        with a message saying that the count is not specified, if it does it checks if the count is in the values
        dictionary, if it isn't it returns a response with a message saying that the count is wrong, if it is it checks if
        the user has a voter profile, if it doesn't it returns a response with a message saying that the user doesn't have a
        voter profile, if it does it checks if the user has paid, if it hasn't it returns a response with a message saying
        that the user has already paid, if it has it gets or creates a pay object with the profile and the EDP_AMOUNT equal
        to the value of the count in the values dictionary, it then serializes the data and returns a response with the
        serialized data and a status code of 200

        :param request: The request object
        """
        count = request.query_params.get("count", None)
        if count is None:
            return Response("Քանակը նշված չէ", status.HTTP_400_BAD_REQUEST)

        if count not in values.keys():
            return Response("Քանակի սխալ", status.HTTP_400_BAD_REQUEST)
        try:
            voter_profile = VoterProfile.objects.get(user_id=request.user.id)
        except VoterProfile.DoesNotExist:
            return Response("Օգտատերը ընտրողի էջ չունի", status.HTTP_400_BAD_REQUEST)
        else:
            if voter_profile.is_paid:
                return Response(
                    "Օգտատերը արդեն վճարել է Քվեարկության համար ",
                    status.HTTP_400_BAD_REQUEST,
                )
            data = Pay.objects.get_or_create(
                profile=voter_profile, EDP_AMOUNT=values[count]
            )
            serializer = PaySerializer(data[0])
            return Response(serializer.data, status=status.HTTP_200_OK)


class PAYAPIView(APIView):
    @csrf_exempt
    def post(self, request):
        """
        If the request is a precheck, check if the transaction exists and if the amount and account are correct. If the
        request is a confirmation, check if the checksum is correct and if it is, confirm the transaction

        :param request: The request object
        :return: The response is a string.
        """
        # precheck data
        EDP_PRECHECK = request.data.get("EDP_PRECHECK", None)
        EDP_BILL_NO = request.data.get("EDP_BILL_NO", None)
        EDP_AMOUNT = request.data.get("EDP_AMOUNT", None)
        EDP_REC_ACCOUNT = request.data.get("EDP_REC_ACCOUNT", None)
        # confirm data
        EDP_PAYER_ACCOUNT = request.data.get("EDP_PAYER_ACCOUNT", None)
        EDP_TRANS_ID = request.data.get("EDP_TRANS_ID", None)
        EDP_CHECKSUM = request.data.get("EDP_CHECKSUM", None)
        if None not in (EDP_PRECHECK, EDP_BILL_NO, EDP_AMOUNT, EDP_REC_ACCOUNT):
            if EDP_PRECHECK == "YES":
                try:
                    trans = Pay.objects.get(EDP_BILL_NO=EDP_BILL_NO)
                except Pay.DoesNotExist:
                    return HttpResponse("Incorrect EDP_BILL_NO")
                else:
                    if (
                        trans.EDP_AMOUNT == EDP_AMOUNT
                        and trans.EDP_REC_ACCOUNT == EDP_REC_ACCOUNT
                    ):
                        print("returning ok")
                        return HttpResponse("OK")
        print("request come")
        if None not in (
            EDP_BILL_NO,
            EDP_AMOUNT,
            EDP_REC_ACCOUNT,
            EDP_PAYER_ACCOUNT,
            EDP_TRANS_ID,
            EDP_CHECKSUM,
        ):
            print("request come")
            EDP_REC_ACCOUNT = str(settings.EDP_REC_ACCOUNT)
            text_to_hash = (
                EDP_REC_ACCOUNT
                + ":"
                + EDP_AMOUNT
                + ":"
                + settings.IDRAM_SKEY
                + ":"
                + EDP_BILL_NO
                + ":"
                + EDP_PAYER_ACCOUNT
                + ":"
                + EDP_TRANS_ID
                + ":"
                + request.data.get("EDP_TRANS_DATE")
            )
            if EDP_CHECKSUM == md5(text_to_hash.encode()).hexdigest().upper():
                print("request come")
                trans = Pay.objects.get(EDP_BILL_NO=EDP_BILL_NO)
                trans.confirmed = True
                trans.save()
                user_profile = trans.profile
                user_profile.is_paid = True
                user_profile.save()
                return HttpResponse("OK")
            else:
                return Response("NO!")
