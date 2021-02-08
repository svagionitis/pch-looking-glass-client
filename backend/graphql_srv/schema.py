import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import Ixp as IxpModel


class Ixp(SQLAlchemyObjectType):
    class Meta:
        model = IxpModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    ixps = graphene.List(Ixp)

    def resolve_ixps(parent, info):
        query = Ixp.get_query(info)
        return query.all()


class Subscription(graphene.ObjectType):
    ixps = graphene.List(Ixp)

    def resolve_ixps(parent, info):
        query = Ixp.get_query(info)
        return query.all()


schema = graphene.Schema(query=Query, subscription=Subscription)
