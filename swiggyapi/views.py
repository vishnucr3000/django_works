from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from swiggyapi.serializers import ProductSerializer
from swiggyapi.models import Products

# Create your views here.

class ProductsView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        seralizer=ProductSerializer(qs,many=True)
        return Response(data=seralizer.data)

    def post(self,request,*args,**kwargs):
       serializer=ProductSerializer(data=request.data)
       if serializer.is_valid():
           Products.objects.create(**serializer.validated_data)
           return Response(data=serializer.data)
       else:
           return Response(data=serializer.errors)

class ProductDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Products.objects.get(id=id)
        serialzer=ProductSerializer(qs)
        return Response(data=serialzer.data)
