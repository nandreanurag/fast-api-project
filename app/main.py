from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db
from .routers import posts, users, auth

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print("DB connection error ", e)

app = FastAPI()

@app.get("/healthz")
async def root(db: Session = Depends(get_db)):
    try:
        return {"message": "Hello world!!"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
