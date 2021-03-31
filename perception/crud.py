from sqlalchemy.orm import Session



from perception import models, schemas


def check_file_id(db: Session, file_id: int):

    try:

        result = db.query(models.Food).filter(models.Food.file_id == file_id).first() 
        
        return result
    
    except Exception as error:
        print(repr(error))

def get_food_by_index_id(db: Session, index_id: int):

    try:
        return db.query(models.Food).filter(models.Food.index_id == int(index_id)).first()

    except Exception as error:
        print(repr(error))


def create_food(db: Session, food: schemas.FoodCreate, index_id: int):
    
    try:
            
        db_food = models.Food(index_id=index_id, file_id=food.file_id, name=food.name, image_url=food.image_url)
        db.add(db_food)
        db.commit()
        db.refresh(db_food)
        return db_food

    except Exception as error:
        print(repr(error))


