import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DB_URL=os.path.join(ROOT_PATH,'db.db')
engine = create_engine(f"sqlite:///{DB_URL}",echo=True)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

class Users(Base):
    __tablename__="users"
    id = Column(Integer(),primary_key=True)
    name = Column(String())

SessionLocal =sessionmaker(bind=engine)
