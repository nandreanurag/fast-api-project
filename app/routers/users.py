from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.userService import user_service
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
        filter_user = user_service.get_user_by_email_Id(email=user.email, db=db)
        if filter_user:
            raise UserAlreadyExistsException(f"User with email: {user.email} already Exists!")
        new_user = user_service.create_user(user=user,db=db)
        return new_user
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="internal Server Error")


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        user = user_service.get_user_by_Id(id=id, db=db)
        if not user:
            raise DataNotFoundException(f"Post with id: {id} Not Found!")
        return user
    except DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
