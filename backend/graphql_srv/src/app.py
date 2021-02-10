from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_sockets import Sockets
from graphql_ws.gevent import GeventSubscriptionServer

from database import db_session
from schema import schema

app = Flask(__name__)
CORS(app)
app.debug = True
sockets = Sockets(app)

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

subscription_server = GeventSubscriptionServer(schema)
app.app_protocol = lambda environ_path_info: "graphql-ws"


@sockets.route("/subscriptions")
def echo_socket(ws):
    subscription_server.handle(ws)
    return []


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
