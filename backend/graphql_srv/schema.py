import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import Ixp as IxpModel


class Ixp(SQLAlchemyObjectType):
    class Meta:
        model = IxpModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):

    node = graphene.relay.Node.Field()
    ixps = SQLAlchemyConnectionField(Ixp.connection)


schema = graphene.Schema(query=Query)
