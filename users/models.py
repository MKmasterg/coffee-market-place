from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class CustomUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)
    id_number = models.CharField(max_length=10)
    date_joined = models.DateTimeField()
    def __str__(self):
        return str(self.user.username)

class Market(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    rate = models.IntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    number_of_orders = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Seller(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    markets = models.ManyToManyField(Market,related_name="markets_seller_set")
    supervisor = models.ManyToManyField(Market,related_name="supervisor_seller_set")
    def __str__(self):
        return str(self.user.user.username)

class Stock(models.Model):
    name = models.CharField(max_length=40)
    desc = models.CharField(max_length=100)
    no = models.IntegerField()
    is_available = models.BooleanField(default=False)
    market = models.ForeignKey(Market,on_delete=models.CASCADE)
    ppg = models.CharField(max_length=50) #price per gram
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    home_address = models.CharField(max_length=100)
    basket = models.ManyToManyField(Stock,blank=True)
    def __str__(self):
        return str(self.user.user.username)

class Order(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    market = models.ForeignKey(Market,on_delete=models.CASCADE)
    number_of_stock = models.IntegerField()
    date_placed = models.DateTimeField()
    class Status(models.IntegerChoices):
        PENDING = 300
        DELIVERED = 200
        DECLINED = 403
    status = models.IntegerField(choices=Status.choices)
    message = models.CharField(max_length=200)
    def __str__(self):
        return str(self.customer.user.user.username)
