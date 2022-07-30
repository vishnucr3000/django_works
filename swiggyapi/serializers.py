from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    product_name = serializers.CharField()
    category = serializers.CharField()
    price = serializers.IntegerField()
    rating = serializers.FloatField()
