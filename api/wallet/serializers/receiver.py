from  rest_framework import  serializers


from apps.wallet.models import ReceiverCardModel


class ReceiverSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    type = serializers.IntegerField()


class ReceiverModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiverCardModel
        fields = ['id','card_number', 'type','card_mask','pc_type','card_name']
