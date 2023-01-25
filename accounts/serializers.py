from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import APIException

from accounts.models import CandidatePost, CandidateProfile, User, VoterProfile


__all__ = (
    "CreateUserSerializer",
    "VoterProfileSerializer",
    "CandidateProfileSerializer",
    "CandidatePostSerializer",
    "LoginSerializer",
)


class PasswordsMismatch(APIException):
    status_code = 403
    default_detail = "Passwords mismatch"


class CreateUserSerializer(serializers.ModelSerializer):
    """This class is a serializer that takes in a model and serializes it into JSON."""

    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password_confirm"]
        wro_settings = {"write_only": True}
        extra_kwargs = {"password": wro_settings, "password_confirm": wro_settings}

    def create(self, validated_data):
        """
        If the password and password_confirm fields match, create a new user with the email and password provided,
        otherwise raise a PasswordsMismatch exception

        :param validated_data: The data that has been validated by the serializer
        :return: The user object is being returned.
        """
        if validated_data["password"] == validated_data["password_confirm"]:
            user = User(
                email=validated_data["email"],
                is_active=True,
            )
            user.set_password(validated_data["password"])
            user.save()
            return user
        else:
            raise PasswordsMismatch()


class VoterProfileSerializer(serializers.ModelSerializer):
    """This class is a serializer for the VoterProfile model."""

    class Meta:
        model = VoterProfile
        exclude = ("is_email_verified", "is_paid")

    def create(self, validated_data):
        """
        The function takes in a validated_data dictionary, unpacks it into a VoterProfile object, saves it to the database,
        and returns the VoterProfile object

        :param validated_data: The data that has been validated by the serializer
        :return: The voter_profile object is being returned.
        """
        voter_profile = VoterProfile(**validated_data)
        voter_profile.save()
        return voter_profile

    def update(self, instance, validated_data):
        """
        It takes an instance of the model and a dictionary of validated data, and updates the instance with the validated
        data

        :param instance: The instance of the model that is being updated
        :param validated_data: The data that has been validated by the serializer
        :return: The instance is being returned.
        """
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance


class CandidatePostSerializer(serializers.ModelSerializer):
    """This class is a serializer for the CandidatePost model."""

    class Meta:
        model = CandidatePost
        fields = "__all__"

    def create(self, validated_data):
        """
        It takes the validated data and creates a new instance of the CandidatePost model

        :param validated_data: The data that has been validated by the serializer
        :return: The post is being returned.
        """
        post = CandidatePost(**validated_data)
        post.save()
        return post

    def update(self, instance, validated_data):
        """
        It takes an instance of the model and a dictionary of validated data, and updates the instance with the validated
        data

        :param instance: The instance of the model that is being updated
        :param validated_data: The data that has been validated by the serializer
        :return: The instance is being returned.
        """
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance


class CandidateProfileSerializer(serializers.ModelSerializer):
    """A serializer class that is used to serialize the data from the model."""

    class Meta:
        model = CandidateProfile
        exclude = ("is_email_verified",)

    def create(self, validated_data):
        """
        It creates a new instance of the CandidateProfile model, saves it to the database, and returns the newly created
        instance

        :param validated_data: The data that has been validated by the serializer
        :return: The candidate_profile object is being returned.
        """
        candidate_profile = CandidateProfile(**validated_data)
        candidate_profile.save()
        return candidate_profile

    def update(self, instance, validated_data):
        """
        It takes an instance of the model and a dictionary of validated data, and updates the instance with the validated
        data

        :param instance: The instance of the model that is being updated
        :param validated_data: The data that has been validated by the serializer
        :return: The instance is being returned.
        """
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """This class is a serializer that takes in email and password and returns a user."""

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """
        If the user exists, is active, and the password is correct, return the user. Otherwise, raise an error

        :param attrs: The validated data from the serializer
        :return: The user object is being returned.
        """
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Օգտատերը գոյություն չունի")
        if user.is_active:
            user = authenticate(email=attrs["email"], password=attrs["password"])
            if user is None:
                raise serializers.ValidationError("Սխալ մուտքանուն կամ գաղտնաբառ")
        else:
            raise serializers.ValidationError("Մուտքը արգելված է")
        return {"user": user}


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
