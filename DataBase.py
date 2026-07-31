from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



'''
Initialize the database
'''

engine = create_engine("mysql+mysqlconnector://Database/visual_db", echo=False, future=True)
Base = declarative_base()
sessionlocal = sessionmaker(bind=engine)
session = sessionlocal()
