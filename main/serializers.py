from rest_framework import serializers


class UserQuerySerializer(serializers.Serializer):
    query = serializers.CharField()