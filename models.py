from database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True) #index=true really accelaret search result
    username = Column(String, unique=True)
    hashed_password = Column(String)
    session_id = Column(String)
    
    

    
class CreateUserRequest(BaseModel):
    username: str
    password: str

    
    

    
    
    
    