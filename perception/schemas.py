from typing import List, Optional

from pydantic import BaseModel

class FoodBase(BaseModel):
    pass

class FoodCreate(FoodBase):
    name: str
    file_id: str
    embedding: List[float]

class Food(FoodBase):
    id: int

    

    class Config:
        orm_mode = True

class SearchResult(BaseModel):
    index_ids: List[int]

class SearchQuery(BaseModel):
    value: List[float]
    