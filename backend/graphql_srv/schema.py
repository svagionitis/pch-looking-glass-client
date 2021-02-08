import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import Ixp as IxpModel


class Ixp(SQLAlchemyObjectType):
    class Meta:
        model = IxpModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):

    node = graphene.relay.Node.Field()
    ixps = graphene.List(Ixp)

    @staticmethod
    def resolve_ixps(parent, info, **args):
        ixps_query = Ixp.get_query(info)

        return ixps_query.all()


schema = graphene.Schema(query=Query, types=[Ixp])
