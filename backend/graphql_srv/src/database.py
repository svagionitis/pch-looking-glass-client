from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import scoped_session, sessionmaker

from config_arg import parse_input_args

conf = parse_input_args()


def create_postgres_db_connection_string(config):
    """
    Create the postgres DB connection string

    NOTE: The usual connection string is like the following

    postgresql://$USER:$PASS@$HOST:$PORT/$DB_NAME

    Now, in the password there is a @ and it will cause problems with the @$HOST,
    so we choose to use the following connection string

    postgresql:///$DB_NAME?host=$HOST&port=$PORT&user=$USER&password=$PASS

    See https://www.postgresql.org/docs/10/libpq-connect.html#LIBPQ-CONNSTRING

    config: The configuration options to create the string

    """
    return "postgresql:///{0}?host={1}&port={2}&user={3}&password={4}".format(
        config.db_name, config.db_host, config.db_port, config.db_user, config.db_pass
    )


db_connection_string = create_postgres_db_connection_string(conf)
engine = create_engine(db_connection_string)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base(cls=DeferredReflection)
Base.query = db_session.query_property()
