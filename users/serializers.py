from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "phone", "city", "avatar")

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            phone=validated_data.get("phone"),
            city=validated_data.get("city"),
            avatar=validated_data.get("avatar"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
