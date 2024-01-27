from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import models, schemas
from app.utils import pwd_context


class userService:

    def get_user_by_email_Id(self, email: str, db: Session) -> Any:
        """ Get User Data based on email"""
        try:
            data = db.query(models.User).filter(
                models.User.email == email).first()
            return data
        except SQLAlchemyError as e:
            return None

    def get_user_by_Id(self, id: int, db: Session) -> Any:
        """ Get User Data based on email"""
        try:
            data = db.query(models.User).filter(models.User.id == id).first()
            print("Data: ", data)
            return data
        except SQLAlchemyError as e:
            print(e)
            return None

    def create_user(self, user: schemas.UserCreate, db: Session) -> Any:
        try:
            hashed_user_pass = pwd_context.hash(user.password)
            user.password = hashed_user_pass
            new_user = models.User(**user.dict())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            print(e)
            return None




user_service = userService()
