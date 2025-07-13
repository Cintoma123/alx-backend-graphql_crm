from .models import 
    Customer,
    Product,
    Order,
from graphene import ObjectType, String, Int, Float, DateTime, Field, List, ID
from graphene_django.types import DjangoObjectType
from django.db import transaction
from crm.schema import Customer, Product, Order


class CustomerType(ObjectType):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductType(ObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class OrderType(ObjectType):
    class Meta:
        model = Order
        fields = "__all__"
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()
        customer = graphene.Field(CustomerType)

    def mutate(self, info, name, email, phone=None):

        if not name or not email:
            raise Exception("Name and email are required fields.")
        if Customer.objects.filter(email=email).exists():
            raise Exception("A customer with this email already exists.")

        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer)
        print("Customer created:", customer)

    class BulkCreateCustomers(graphene.Mutation):
        class Arguments:
            customers = List(CustomerType)
        def mutate(self, info, customers):
            customer = graphene.List(CustomerType , required=True)
        """ validate customer data"""
        try:
            if not name or not email:
                errors.append({"index": "idx", "email": "Email is missing"})
                raise Exception("Name and email are required fields.")
            with transaction.atomic():
                for customer_data in customers:
                    if Customer.objects.filter(email=customer_data.email).exists():
                        raise Exception(f"Customer with email {customer_data.email} already exists.")
                    customer = Customer(
                        name=customer_data.name,
                        email=customer_data.email,
                        phone=customer_data.phone
                    )
                    customer.save()
                    customer_list.append(customer)
            return CreateCustomer(customer=customer_list)
        except Exception as e:
            raise Exception(f"An error occurred while creating customers: {str(e)}")
    class CreateProduct(graphene.Mutation):
        class Arguments:
            name = graphene.String(required=True)
            description = graphene.String()
            price = graphene.Float(required=True)
            stock = graphene.Int(default_value=0)
            product = graphene.Field(ProductType)

        def mutate(self, info, name, price, description=None, stock=0):
            if not name or price is None:
                raise Exception("Name and price are required fields.")
            product = Product(name=name, description=description, price=price, stock=stock)
            product.save()
            return CreateProduct(product=product)
    class CreateOrder(graphene.Mutation):
        """Create an order for a customer with a specific product."""
        class Arguments:
            customer_id = graphene.ID(required=True)
            product_id = graphene.ID(required=True)
            order = graphene.Field(OrderType)
        def mutate(self, info, customer_id, product_id):
            try:
                if not customer_id or not product_id:
                    raise Exception("Customer ID and Product ID are required fields.")
                customer = Customer.objects.get(id=customer_id)
                product = Product.objects.get(id=product_id)
                order = Order.objects.create(
                    customer_id=customer,
                    product_id=product
                )
                total_amount = product.price + (product.price * 0.1)  # Example: adding 10% tax
                order.total_amount = total_amount
                order.save()
                return CreateOrder(order=order)
            """except Customer.DoesNotExist:
                raise Exception(f"Customer with ID {customer_id} does not exist.")
            except Product.DoesNotExist:
                raise Exception(f"Product with ID {product_id} does not exist.")
            except Exception as e:
                raise Exception(f"An error occurred while creating the order: {str(e)}")"""
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = CreateCustomer.BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    def resolve_all_customers(self, info):
        return Customer.objects.all()

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_all_orders(self, info):
        return Order.objects.all()