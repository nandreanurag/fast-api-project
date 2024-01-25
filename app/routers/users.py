from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import pwd_context
from execeptions.DataNotFoundException import DataNotFoundException
from execeptions.UserAlreadyExistsException import UserAlreadyExistsException

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        filter_user = db.query(models.User).filter(models.User.email == user.email)
        if filter_user.first():
            raise UserAlreadyExistsException(f"User with email: {user.email} already Exists!")
        hashed_user_pass = pwd_context.hash(user.password)
        user.password = hashed_user_pass
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="internal Server Error")


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise DataNotFoundException(f"Post with id: {id} Not Found!")
        return user
    except DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
