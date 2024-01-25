from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db

# we need below 3 things for creating token
# SECRET KEY
# Algo
# Expiration time

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id = payload.get("user_id")
        # print("Token Id: "+str(id))
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        # print("Token data: "+token_data.id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail=f"Could not validate Credentials")
    user_id = verify_access_token(token, credentials_exception)
    # print(user_id)
    # db.query(models.User).filter(models.User.email == user.email)
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    # print(user.id)
    return user
