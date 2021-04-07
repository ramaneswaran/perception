import os
import json
import yaml
from typing import List

from PIL import Image
import io

import numpy as np
import shutil

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi import File, Body, Response, File, UploadFile

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseSettings

import uvicorn

from sqlalchemy.orm import Session

from perception import crud, models, schemas
from perception.database import SessionLocal, engine
from perception.core.faiss_helper import FaissCore

from perception.encoders.conv import VGGEncoder

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
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

index = FaissCore(name=settings.index_name, store=settings.index_store_path, dimension=settings.dimension)
encoder = VGGEncoder()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def read_metadata(file_id: str):
    """
    Reads metadata file
    """

    meta_store = './perception/data_store/recipes'
    file_name = f"meta{file_id.zfill(5)}.json"
    file_path = os.path.join(meta_store, file_name)

    with open(file_path) as f:
        data = json.load(f)
    
    return data 

@app.post("/food/insert", response_model=schemas.Food)
def create_food(food: schemas.FoodCreate, db: Session = Depends(get_db)):
    

    vector = np.array(food.embedding)

    index_id = index.insert(vector)

    if crud.check_file_id(db=db, file_id=food.file_id):
        raise HTTPException(status_code = 409, detail=  "This file ID already exists")

    return crud.create_food(db=db, food=food, index_id=index_id-1)


# @app.post("/food/search",response_model=schemas.SearchResult)
# def search_food(query: schemas.SearchQuery,  db: Session = Depends(get_db)):
    
#     vector = np.array(query.value)

#     index_ids = index.search(vector,4)
#     food_items = []
#     for index_id in index_ids[0]:
        
#         if index_id != -1:
#             item = crud.get_food_by_index_id(db,index_id)
#             if item is not None:
              
#                 food_items.append(schemas.Food.from_orm(item))

#     result = schemas.SearchResult(result=food_items, index_ids=index_ids[0].tolist())

#     return result


@app.get("/",  response_class=HTMLResponse)
async  def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/result",  response_class=HTMLResponse)
async  def result(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})

@app.post("/food/search/result", response_class=HTMLResponse)
async def search_with_image(request: Request, image: UploadFile = File(...), db: Session = Depends(get_db) ):

    with open("out.png", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    image_data = Image.open("out.png").convert("RGB")
    feature = encoder.encode(image_data)


    index_ids = index.search(feature,4)
    food_items = []
    for index_id in index_ids[0]:
        
        if index_id != -1:
            item = crud.get_food_by_index_id(db,index_id)
            if item is not None:
              
                food_items.append(schemas.Food.from_orm(item))

    return templates.TemplateResponse("result.html", {"request": request, "food_items": food_items})

@app.get("/food/search/upload", response_class=HTMLResponse)
async def search_view(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.get('/food/{food_id}/recipe', response_class=HTMLResponse)
async def recipe_view(food_id: str, request: Request):
    data = read_metadata(food_id)
    return templates.TemplateResponse("recipe.html", {"request": request, "data":data})