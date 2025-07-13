import graphene
from graphene import ObjectType, Schema
from graphene_django.types import DjangoObjectType

class Query(ObjectType):
    class Meta:
        field = (name:'hello', Types:'world')