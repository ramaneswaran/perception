import os
from typing import List

import numpy as np

from fastapi import Depends, FastAPI, HTTPException
from fastapi import File, Body, Response

from pydantic import BaseSettings

import uvicorn

from sqlalchemy.orm import Session

from perception import crud, models, schemas
from perception.database import SessionLocal, engine
from perception.core.faiss_helper import FaissCore

models.Base.metadata.create_all(bind=engine)



class Settings(BaseSettings):
    app_name: str = "Perception"
    base_dir: str = os.path.dirname(os.path.realpath(__file__))
    index_store_path: str = os.path.join(base_dir, "index_store")
    index_name: str = "vector.index"


settings = Settings()

app = FastAPI()
index = FaissCore(name=settings.index_name, store=settings.index_store_path, dimension=6)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/food/insert", response_model=schemas.Food)
def create_food(food: schemas.FoodCreate, index_file: str = Body(...), dimension: int = Body(...), db: Session = Depends(get_db)):
    

    vector = np.array(food.embedding)

    index_id = index.insert(vector)

    return crud.create_food(db=db, food=food, index_id=index_id)


@app.post("/food/search",response_model=schemas.SearchResult)
def search_food(query: List[float] = Body(...), index_file: str = Body(...), dimension: int = Body(...), db: Session = Depends(get_db)):
    
    vector = np.array(query)


    index_ids = index.search(vector,4)

    result = schemas.SearchResult(index_ids=index_ids[0].tolist())

    return result
