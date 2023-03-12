from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    developer = Column(String)