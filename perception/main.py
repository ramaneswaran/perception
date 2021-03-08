from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from perception import crud, models, schemas
from perception.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/food/", response_model=schemas.Food)
def create_user(food: schemas.FoodCreate, db: Session = Depends(get_db)):
    
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_food(db=db, food=food)
