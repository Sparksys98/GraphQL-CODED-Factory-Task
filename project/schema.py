import ecommerce.schema
import graphene
import graphql_jwt


class Query(ecommerce.schema.Query, graphene.ObjectType):
    pass


class Mutation(
    ecommerce.schema.Mutation, graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
