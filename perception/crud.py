from sqlalchemy.orm import Session



from perception import models, schemas




def get_food(db: Session, food_id: int):

    try:

        return db.query(models.Food).filter(models.Food.id == food_id).first()

    except Exception as error:
        print(repr(error))


def create_food(db: Session, food: schemas.FoodCreate):
    
    try:
            
        db_food = models.Food(index_id=food.index_id, image=food.image, recipe=food.recipe)
        db.add(db_food)
        db.commit()
        db.refresh(db_food)
        return db_food

    except Exception as error:
        print(repr(error))


