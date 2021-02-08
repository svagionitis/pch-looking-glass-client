from flask import Flask
from flask_cors import CORS
from database import db_session
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
CORS(app)
app.debug = True

example_query = """
{
  ixps {
    ixp
    ixpCity
    ixpCountry
    ixpIpVersion
    ixpLocalAsn
    ixpRibEntries
    ixpNumberOfPeers
    ixpNumberOfNeighbors
    dateAdded
  }
}
"""

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema, graphiql=True, context={"session": db_session}
    ),
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run()
