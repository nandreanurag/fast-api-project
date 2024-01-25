from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import UserLogin
from execeptions.DataNotFoundException import DataNotFoundException
from .. import database, models, utils, oauth2, schemas

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)


# Instead of passing user_cred in body we can use inbuilt feature of fast API
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    try:
        # OAuth2PasswordRequestForm has 2 fields 1.username, password
        user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
        print(user)
        if not user:
            raise DataNotFoundException(f"User with email Id: {user_credentials.username} Not Found!")
        if utils.verify(user_credentials.password, user.password):
            access_token = oauth2.create_access_token(data={"user_id": user.id})
            return schemas.Token(access_token= access_token, token_type= "bearer")
            # return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Invalid Login Credentials!")

    except DataNotFoundException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
