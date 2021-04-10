from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.CharField(max_length=400, null=True)

    def __str__(self):
      return self.name

class OrderProduct(models.Model):
    order = models.ForeignKey("Orders", on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order_quantity} of {self.product.name}" 

class Orders(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through=OrderProduct)
    is_checked_out = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.now())
    
    class Meta: 
        verbose_name_plural = "orders"

    def __str__(self):
        return self.user.username + " "+"order"

# Create a cart on user create
@receiver(post_save, sender=get_user_model())
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Orders.objects.create(user=instance)