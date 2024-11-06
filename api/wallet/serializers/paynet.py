from rest_framework import serializers

from apps.wallet.models.paynet import Category, Providers


class ProvidersSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()


class CategoriesSerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = ['id', 'title_ru', 'title_uz', 'is_subcategory', 'category_id','is_active']




class ProviderSerializer(serializers.ModelSerializer):


    class Meta:
        model = Providers
        fields = ['id', 'title', 'title_short', 'provider_id', 'category_id',]




class ServersSerializer(serializers.Serializer):
    provider_id = serializers.IntegerField()

#comment
class ServerSearchSerializer(serializers.Serializer):
    search_text = serializers.CharField(help_text="example uz or rus")


class CheckReceiverSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    fields = serializers.DictField()


class PaymentSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=200)
    service_id = serializers.IntegerField()
    fields = serializers.DictField()


class PaymentConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    sender_ext = serializers.CharField(max_length=200)
    receiver_ext = serializers.CharField(max_length=200)
