import graphene
from graphene import ObjectType, Schema
from graphene_django.types import DjangoObjectType
import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
"""class Query(ObjectType):
    class Meta:
        field = (name:'hello', Types:'world')"""