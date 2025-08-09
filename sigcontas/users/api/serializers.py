from rest_framework import serializers
from sigcontas.users.models import User
from django.contrib.auth.models import Group


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "name", "email", "groups"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ["username", "password", "name", "email", "groups"]

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        user = User.objects.create_user(**validated_data)
        user.groups.set(groups)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = ["name", "email", "groups"]

    def update(self, instance, validated_data):
        groups = validated_data.pop("groups", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if groups is not None:
            instance.groups.set(groups)
        return instance

        fields = ("id", "username", "email", "is_staff", "is_active", "date_joined", "name", "is_professor")