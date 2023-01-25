from rest_framework import serializers

from accounts.models import User, VoterProfile

from .models import CandidateProfile, EvaluateModel, MarkModel, News, PayViaImage


__all__ = [
    "MarkModelSerializer",
    "EvaluateModelSerializer",
    "NewsSerializer",
    "CandidateProfilesSerializer",
    "PayViaImageSerializer",
]


class MarkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkModel
        fields = "__all__"


class EvaluateModelSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        """
            check if request sent user candidate profile verified

        :param attrs: request data
        :return: request data if success otherwise rise exception
        """
        if not User.objects.get(candidateprofile=attrs["candidate"]).is_candidate:
            raise serializers.ValidationError(
                "candidate profile not exist or not confirmed"
            )

        return attrs

    class Meta:
        model = EvaluateModel
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class CandidateProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        exclude = ("is_email_verified",)


class PayViaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayViaImage
        fields = "__all__"
