from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ["id", "username", "email", "name", "is_professor", "is_active", "is_staff"]
        read_only_fields = ["id", "is_active", "is_staff"]

        fields = '__all__'

