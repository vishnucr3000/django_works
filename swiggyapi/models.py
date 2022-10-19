from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import datetime,timedelta


# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    price = models.PositiveIntegerField()



    def __str__(self):
        return self.product_name

    def review_avg(self):
        all_reviews=self.review_set.all()
        if all_reviews:
            rating=sum([review.rating for review in all_reviews])
            return rating/len(all_reviews)
        else:
            return 0

    def review_count(self):
        return self.review_set.all().count()

class Review(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    comment=models.CharField(max_length=250)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    class Meta:
        unique_together=("author","product")

class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    asondate=models.DateField(auto_now_add=True)
    qty=models.PositiveIntegerField(validators=(MinValueValidator(1),MaxValueValidator(10)))
    options=(
        ("in_cart","in_cart"),
        ("order_placed","order_placed"),
        ("completed","completed")
    )
    status=models.CharField(max_length=20,choices=options,default="in-cart")

class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    order_date=models.DateField(auto_now_add=True)
    options=(
        ("Order_Placed","Order Placed"),
        ("Despatched","Despathced"),
        ("In_Transit","In Transit"),
        ("Delivered","Delivered")
    )

    status=models.CharField(max_length=20,choices=options,default="Order Placed")
    edd=datetime.today()+timedelta(days=5)
    expected_delivery_date=models.DateField(default=edd)





