import django_filters
from .models import Customer , Product , Order
from graphene import ObjectType, List
from graphene_django.types import DjangoObjectType
from django.db import transaction
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from .types import CustomerType, ProductType, OrderType
from .filters import CustomerFilter, ProductFilter, OrderFilter


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    created_at__gte = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_at__lte = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    phone_pattern = django_filters.CharFilter(method='filter_phone_pattern')

    def filter_phone_pattern(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)

    class Meta:
        model = Customer
        fields = ['name', 'email', 'created_at', 'phone_pattern']

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    stock__gte = django_filters.NumberFilter(field_name="stock", lookup_expr='gte')
    stock__lte = django_filters.NumberFilter(field_name="stock", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

class OrderFilter(django_filters.FilterSet):
    customer_id = django_filters.NumberFilter(field_name="customer__id")
    product_id = django_filters.NumberFilter(field_name="product__id")
    order_date__gte = django_filters.DateFilter(field_name="order_date", lookup_expr='gte')
    order_date__lte = django_filters.DateFilter(field_name="order_date", lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['customer_id', 'product_id', 'order_date']
        # Add any additional fields you want to filter by
        # e.g., 'status', 'total_amount', etc.

class Query(graphene.ObjectType):
   all_customers = DjangoFilterConnectionField(CustomerType, filterset_class=CustomerFilter)
   all_ products = DjangoFilterConnectionField(ProductType, filterset_class=ProductFilter)
   all_orders = DjangoFilterConnectionField(OrderType, filterset_class=OrderFilter)

    def resolve_customers(self, info, **kwargs):
        return Customer.objects.all()

    def resolve_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_orders(self, info, **kwargs):
        return Order.objects.all()