from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VideoCard(Base):
    __tablename__ = "videocards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manufacturer = Column(String)
    memory = Column(Integer)
    price = Column(Float)
    description = Column(String)

class CPU(Base):
    __tablename__ = "cpus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manufacturer = Column(String)
    cores = Column(Integer)
    clock_speed = Column(Float)
    price = Column(Float)
    description = Column(String)