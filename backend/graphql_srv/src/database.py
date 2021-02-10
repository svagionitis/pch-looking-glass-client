from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import scoped_session, sessionmaker

# See https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
# db_connection_string = "postgresql://ixp:PchL00k1ngGl\@ss@localhost/ixp"
db_connection_string = (
    "postgresql:///ixp?user=ixp&password=PchL00k1ngGl@ss&host=localhost"
)
engine = create_engine(db_connection_string)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base(cls=DeferredReflection)
Base.query = db_session.query_property()
