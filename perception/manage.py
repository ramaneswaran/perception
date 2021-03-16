import os 

from sqlalchemy.orm import Session
from perception.database import SessionLocal, engine

from perception import models, schemas
from perception.core.faiss_helper import FaissCore

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_food_by_index_id(db: Session, index_id: int):
    try:

        return db.query(models.Food).filter(models.Food.index_id == index_id).first()

    except Exception as error:
        print(repr(error))

def check_file_id(db: Session, file_id: int):

    try:

        result = db.query(models.Food).filter(models.Food.file_id == file_id).first() 
        
        return result
    
    except Exception as error:
        print(repr(error))

if __name__ == "__main__":
    db = db = SessionLocal()
    indexes = [0,1]

    result = get_food_by_index_id(db, 0)
    # result = db.query(models.Food).all()

    # for obj in result:
    #     print(schemas.Food.from_orm(obj))

    print(result.index_id)


    # base_dir = os.path.dirname(os.path.realpath(__file__))
    # index_store = os.path.join(base_dir, 'index_store')
    # index = FaissCore('vector.index',index_store, dimension=6)

    # print(index.size)