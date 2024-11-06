# serializers.py
from rest_framework import serializers

from apps.wallet.models import TransactionsModel


class TransactionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionsModel
        fields = ['id','debit_tr_id', 'db_amount', 'created_at', 'sender', 'cr_amount','db_state','db_description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['sender'] = self.mask_card_number(representation['sender'])
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d')


        return representation

    def mask_card_number(self, card_number):
        card_number_str = str(card_number)
        length = len(card_number_str)

        if length <= 8:
            return card_number_str

        masked_part = '*' * (length - 8)
        return card_number_str[:4] + masked_part + card_number_str[-4:]

class MonitoringCheckSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)


class TransactionsStateSerializer(serializers.Serializer):
    ext_id = serializers.CharField()