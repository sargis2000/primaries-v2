from rest_framework import serializers

from .models import Pay


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"
