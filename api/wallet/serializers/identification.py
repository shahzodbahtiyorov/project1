from rest_framework import serializers

from apps.accounts.models import NotificationModel
from apps.wallet.models import Identification


class IdentificationSerializer(serializers.Serializer):
    code = serializers.CharField()
    image = serializers.CharField(style={'base_template': 'textarea.html'},
                                  required=False)






class IdentificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields = ['response']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = '__all__'