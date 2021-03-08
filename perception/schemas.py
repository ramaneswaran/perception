from typing import List, Optional

from pydantic import BaseModel

class FoodBase(BaseModel):
    pass

class FoodCreate(FoodBase):
    index_id: int
    image: str 
    recipe: str

class Food(FoodBase):
    id: int
    

    class Config:
        orm_mode = True