from sqlalchemy import Integer, String, Column, DateTime
from database import Base

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    price = Column(Integer)
    timestamp = Column(DateTime)

