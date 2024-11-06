from rest_framework import  serializers



class CardExtId(serializers.Serializer):
    ext_id = serializers.CharField()



class TransferReceiverInfo(serializers.Serializer):
    card_number = serializers.CharField()
    amount = serializers.IntegerField()
    currency = serializers.IntegerField()


class TransferCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    amount = serializers.IntegerField()
    currency  = serializers.IntegerField()

class  TransferStateSerializer(serializers.Serializer):
    ext_id = serializers.CharField()
    code = serializers.CharField()
    token = serializers.CharField()



class ReceiverInfoCard(serializers.Serializer):
    card_number = serializers.CharField(required=True,max_length=100)

class TransferCreateRF(serializers.Serializer):
    token = serializers.CharField(max_length=100)
    amount = serializers.IntegerField()
    currency = serializers.IntegerField()
    receiver  = serializers.CharField(max_length=100)