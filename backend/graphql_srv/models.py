from sqlalchemy import Column, String
from database import Base, engine


class Ixp(Base):
    __tablename__ = "ixp_info"
    ixp = Column(String, primary_key=True)
    ixp_city = Column(String, primary_key=True)
    ixp_country = Column(String, primary_key=True)
    ixp_ip_version = Column(String, primary_key=True)


Base.prepare(engine)
