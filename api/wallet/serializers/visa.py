from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CardRegisterSerializer(serializers.Serializer):
    number = serializers.CharField()
    expire = serializers.CharField()


class CardRegisterConfirmSerializer(serializers.Serializer):
    ext_id = serializers.CharField()
    code = serializers.CharField()


class CardBinCheckSerializer(serializers.Serializer):
    number = serializers.CharField()

class CardTokenSerializer(serializers.Serializer):
    token = serializers.CharField()