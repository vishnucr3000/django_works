from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from swiggyapi.serializers import ProductSerializer
from swiggyapi.models import Products, Review
from django.contrib.auth.models import User
from swiggyapi.serializers import ProductModelSerializer, UserModelSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from django.db import IntegrityError


# Create your views here.

class ProductsView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Products.objects.all()
        seralizer = ProductSerializer(qs, many=True)
        return Response(data=seralizer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            Products.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class ProductDetailView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        qs = Products.objects.get(id=id)
        serialzer = ProductSerializer(qs)
        return Response(data=serialzer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        product = Products.objects.filter(id=kwargs.get("id"))
        serialise = ProductSerializer(data=request.data)
        if serialise.is_valid():
            product.update(**serialise.validated_data)
            return Response(data=serialise.validated_data, status=status.HTTP_200_OK)
        else:
            return Response({"msg:Update Failed"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product = Products.objects.get(id=kwargs.get("id"))
        product.delete()
        return Response({"msg:Product Deleted"})


class ProductsModelView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Products.objects.all()
        if "category" in request.query_params:
            qs = qs.filter(category__contains=request.query_params.get("category"))
        if "price_gt" in request.query_params:
            qs = qs.filter(price__gte=request.query_params.get("price_gt"))
        seralizer = ProductModelSerializer(qs, many=True)
        return Response(data=seralizer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductModelDetailView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        product = Products.objects.get(id=id)
        serialize = ProductModelSerializer(product)
        return Response(serialize.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        product = Products.objects.get(id=id)
        serialize = ProductModelSerializer(instance=product, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(data=serialize.validated_data)
        else:
            return Response({"msg:Update Failed"})

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        product = Products.objects.get(id=id)
        product.delete
        return Response({"msg:Product Deleted"})


class ProdcutViewSetView(ViewSet):
    def list(self, request, *args, **kwargs):
        products = Products.objects.all()
        serializer = ProductModelSerializer(products, many=True)
        return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serialize = ProductModelSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(data=serialize.validated_data)
        else:
            return Response(data=serialize.errors)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            product = Products.objects.get(id=id)
            serialize = ProductModelSerializer(product)
            return Response(data=serialize.data)
        except:
            return Response({"msg: Item Not Found"})

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        serializer = ProductModelSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.validated_data)
        else:
            return Response(data=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        product.delete()
        return Response({"msg: Item Deleted"})


# Model View Set

class ProductModelViewSetView(ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Products.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True)
    def get_review(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        review = product.review_set.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(data=serializer.data)

    @action(methods=["post"],detail=True)
    def post_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product=Products.objects.get(id=id)
        author=request.user
        try:
            serializer=ReviewSerializer(data=request.data,context={"author":author,"product":product})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
        except IntegrityError:
            message="Duplicates found"
            return Response(message)


class UserModelView(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
