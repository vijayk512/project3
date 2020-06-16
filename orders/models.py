from django.db import models

# Create your models here.


class Pizza(models.Model):
    pizza_type = models.CharField(max_length=64)
    price_m = models.CharField(max_length=20)
    price_l = models.CharField(max_length=20)
    type = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.pizza_type} - {self.price_m} - {self.price_l} - {self.type}"


class Toppings(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name} - {self.type}"


class Subs(models.Model):
    name = models.CharField(max_length=64)
    price_m = models.CharField(max_length=20)
    price_l = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.price_m} - {self.price_l}"


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Salads(models.Model):
    name = models.CharField(max_length=64)
    price = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Dinner_Platters(models.Model):
    name = models.CharField(max_length=64)
    price_m = models.CharField(max_length=20)
    price_l = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.price_m} - {self.price_l}"


class Orders(models.Model):
    user_id = models.CharField(max_length=64)
    total = models.CharField(max_length=40, null=True)
    status = models.CharField(max_length=20)
    cart_detail = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
