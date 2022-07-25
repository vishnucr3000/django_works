from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from dishes.models import menu_items


# Create your views here.

class DishesView(APIView):
    def get(self, request, *args, **kwargs):

        if "dishname" in request.query_params:
            dishname=request.query_params.get("dishname")
            dish = [dish for dish in menu_items if dish.get("dish_name")==dishname]
            return Response(data=dish)

        if "category" in request.query_params:
            categoryname=request.query_params.get("category")
            dish=[dish for dish in menu_items if dish.get("category")==categoryname]
            return Response(data=dish)

        return Response(data=menu_items)

    def post(self, request, *args, **kwargs):
        newdish = request.data
        menu_items.append(newdish)
        return Response(data=newdish)

class DishDetailView(APIView):
    def put(self,request,*args,**kwargs):
        dishid=kwargs.get("id")
        dish=[dish for dish in menu_items if dish.get("code")==dishid].pop()
        updateddish=request.data
        dish.update(updateddish)
        return Response(data=updateddish)

    def delete(self,request,*args,**kwargs):
        dishid=kwargs.get("id")
        dish=[dish for dish in menu_items if dish.get("code")==dishid].pop()
        menu_items.remove(dish)
        return Response(data=dish)



