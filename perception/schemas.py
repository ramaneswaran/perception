from typing import List, Optional

from pydantic import BaseModel

class FoodBase(BaseModel):
    pass

class FoodCreate(FoodBase):
    name: str
    file_id: str
    image_url: str 
    embedding: List[float]

class Food(FoodBase):
    id: int
    index_id: int
    name: str 
    file_id: str
    image_url: str
    

    class Config:
        orm_mode = True

class SearchResult(BaseModel):
    result: List[Food]
    index_ids: List[int]

class SearchQuery(BaseModel):
    value: List[float]
