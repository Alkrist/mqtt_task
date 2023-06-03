from rest_framework import serializers
from .models import Coin

# Serializace dat


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'

    # Pro editaci záznamu: mění parametry vybrané měny na nové, nebo ponechá je bez změny
    # v případě, že parametr nebyl specifikováný.
    def update(self, instance, validated_data):
        instance.identifier = validated_data.get(
            'identifier', instance.identifier)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.symbol = validated_data.get('symbol', instance.symbol)
        instance.name = validated_data.get('name', instance.name)
        instance.supply = validated_data.get('supply', instance.supply)
        instance.save()
        return instance
