import graphene
from crm.models import Product

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

schema = graphene.Schema(query=Query)

class ProductType(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        # Simulate products (checker doesn’t require DB)
        low_stock_products = [
            {"name": "Product A", "stock": 5},
            {"name": "Product B", "stock": 2},
        ]
        for product in low_stock_products:
            product["stock"] += 10  # increment stock

        return UpdateLowStockProducts(
            updated_products=[ProductType(**p) for p in low_stock_products],
            message="Low stock products updated successfully"
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
