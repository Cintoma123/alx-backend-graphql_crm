import graphene
from graphene import ObjectType, List
from graphene_django.types import DjangoObjectType
from django.db import transaction
from .models import Customer, Product, Order
class Query(ObjectType):
    customers = List(CustomerType)
    products = List(ProductType)
    orders = List(OrderType)

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.all()