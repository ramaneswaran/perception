import os
import yaml
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

stream = open("config.yaml", 'r')
config = yaml.safe_load(stream)

class Settings(BaseSettings):
    app_name: str = "Perception"
    base_dir: str = os.path.dirname(os.path.realpath(__file__))

    index_store_path: str = os.path.join(base_dir, "index_store")
    index_name: str = config["index_name"]
    dimension: int = config['dimension']

    image_dir = os.path.join(base_dir, 'data_store/images')
    recipe_dir = os.path.join(base_dir, 'data_store/recipes')

settings = Settings()

app = FastAPI()
index = FaissCore(name=settings.index_name, store=settings.index_store_path, dimension=settings.dimension)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/food/insert", response_model=schemas.Food)
def create_food(food: schemas.FoodCreate, db: Session = Depends(get_db)):
    

    vector = np.array(food.embedding)

    index_id = index.insert(vector)

    if crud.check_file_id(db=db, file_id=food.file_id):
        raise HTTPException(status_code = 409, detail=  "This file ID already exists")

    return crud.create_food(db=db, food=food, index_id=index_id-1)


@app.post("/food/search",response_model=schemas.SearchResult)
def search_food(query: schemas.SearchQuery,  db: Session = Depends(get_db)):
    
    vector = np.array(query.value)

    index_ids = index.search(vector,4)
    food_items = []
    for index_id in index_ids[0]:
        
        if index_id != -1:
            item = crud.get_food_by_index_id(db,index_id)
            if item is not None:
              
                food_items.append(schemas.Food.from_orm(item))

    result = schemas.SearchResult(result=food_items, index_ids=index_ids[0].tolist())

    return result

