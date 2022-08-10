"""swiggyproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dishes import views as dview
from swiggyapi.views import ProductsView as pview
from swiggyapi.views import ProductDetailView as pdview
from swiggyapi.views import ProductsModelView as pmview
from swiggyapi.views import ProductModelDetailView as pmdview
from rest_framework.routers import DefaultRouter
from swiggyapi.views import ProdcutViewSetView,ProductModelViewSetView,UserModelView
from rest_framework.authtoken.views import obtain_auth_token

router=DefaultRouter()
router.register('swiggyapi/v1/products', ProdcutViewSetView, basename="products")
router.register('swiggyapi/v2/products',ProductModelViewSetView,basename="mproducts")
router.register('swiggyapi/v2/register',UserModelView,basename="register")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swiggy/dishes', dview.DishesView.as_view()),
    path('swiggy/dishdetail/<int:id>', dview.DishDetailView.as_view()),
    path('swiggyapi/products',pview.as_view()),
    path('swiggyapi/products/<int:id>',pdview.as_view()),
    path('swiggyapi/productsmodel',pmview.as_view()),
    path('swiggyapi/productsmodel/<int:id>',pmdview.as_view()),
    path('swiggyapi/token',obtain_auth_token),




]+router.urls
