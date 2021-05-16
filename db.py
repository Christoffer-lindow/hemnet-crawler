from sqlalchemy import create_engine, Column,Boolean, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
def initialize_db(conn_string):
    engine = create_engine(conn_string)
    return engine

class Property(Base):
    __tablename__ = 'stockholm_estates'
    id = Column(Integer, primary_key=True)
    url = Column(String(150))
    img_url = Column(String(150))
    street = Column(String(100))
    address = Column(String(100))
    price =  Column(Float)
    type = Column(String(100))
    contract_type = Column(String(100))
    rooms = Column(Integer)
    area = Column(Float)
    balcony = Column(Boolean)
    year_built = Column(Date)
    rent = Column(Float)
    consumption_price = Column(Float)
    price_sqm = Column(Float)