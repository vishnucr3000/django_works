from rest_framework import serializers
from swiggyapi.models import Products, Review,Carts
from django.contrib.auth.models import User


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField()
    category = serializers.CharField()
    price = serializers.IntegerField()



class ProductModelSerializer(serializers.ModelSerializer):
    review_avg = serializers.CharField(read_only=True)
    review_count = serializers.CharField(read_only=True)
    id=serializers.IntegerField(read_only=True)

    class Meta:
        model = Products
        fields = [
            "id",
            "product_name",
            "category",
            "price",
            "review_avg",
            "review_count",
        ]


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        author = self.context.get("author")
        product = self.context.get("product")
        return Review.objects.create(**validated_data, author=author, product=product)

class CartSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    asondate=serializers.DateField(read_only=True)
    status=serializers.CharField(read_only=True)
    class Meta:
        model=Carts
        fields="__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Carts.objects.create(**validated_data,user=user,product=product)
