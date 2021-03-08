from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from perception.database import Base




class Food(Base):

    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    index_id = Column(Integer, index=True)
    image = Column(String)    
    recipe = Column(String)
    