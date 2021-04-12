import graphene
from django.db.models import Q
from django.contrib.auth.models import User
from graphene import ObjectType, List, Field, String, Int, Float
from graphene_django import DjangoObjectType

from .models import  OrderProduct, Product, Orders


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"
    
    def resolve_description(self, info):
        if info.context.user.is_anonymous:
            return ""
        return self.description

        
class OrderProductType(DjangoObjectType):
    class Meta:
        model = OrderProduct

        
class OrderType(DjangoObjectType):
    class Meta:
        model = Orders


class Query(graphene.ObjectType):
    products = List(ProductType)
    product = Field(ProductType, name= String())
    cart = Field(OrderType,  user_id= Int())
    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_product(self, info, name):
        return Product.objects.get(name=name)

    def resolve_cart(self, info, user_id):
        return Orders.objects.get(user=user_id, is_checked_out=False)

class AddOrderInput(graphene.InputObjectType):
    order_id = Int()
    product_id = Int()
    order_quantity = Int()


class AddOrderProduct(graphene.Mutation):
    addOrderProduct = Field(OrderProductType)

    class Arguments:
        order_data = AddOrderInput(required=True)

    def mutate(self, info, order_data, **kwargs):
        order = OrderProduct.objects.create(**order_data)
        return AddOrderProduct(addOrderProduct=order)


class Checkout(graphene.Mutation):
    checkout = Field(OrderType)
    message = String()

    class Arguments:
        user_id = Int(required=True)

    def mutate(self, info, user_id, **kwargs):
        user = info.context.user
        order = Orders.objects.get(user=user, is_checked_out=False)
        order.is_checked_out=True
        order.save()
        Orders.objects.create(user=user)
        return Checkout(message="uyguyguy", checkout=order)

class Mutation(graphene.ObjectType):
    add_order_product = AddOrderProduct.Field()
    checkout = Checkout.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
