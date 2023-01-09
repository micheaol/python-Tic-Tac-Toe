
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.expression import null
from .database import Base

class Post(Base):
    __tablename__ = "posts"


    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()'))

# class User(Base):
#     __table__ = "users"

#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nollable=False, unique=True)
#     password = Column(String, nollable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()'))