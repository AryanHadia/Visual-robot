# class ke vasl behshe be soton database
from sqlalchemy import Column , String , JSON , Integer
from DataBase import Base

class User(Base):
    '''
    User class
    :param Name: Name of the user
    :param Face_embedding:512 dimensional embedding
    '''
    __tablename__ = 'faces'
    Face_id = Column(Integer, primary_key=True, autoincrement=True , nullable=False)
    Name = Column(String(45), nullable=False  , unique=True , index=True)
    Face_embedding = Column(JSON, nullable=False)       