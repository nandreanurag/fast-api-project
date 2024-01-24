import time

import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from app import models
from app.database import engine
from .routers import posts, users

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='1234',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection is successful")
        break
    except Exception as e:
        print("Connection to DB Failed")
        print(f"Error: {str(e)}")
        time.sleep(10)
my_posts = [{'id': 1, 'title': 'HIMYM', 'content': "Rom Com "},
            {'id': 2, 'title': 'Friends', 'content': "Rom Com Ok!"}]

app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello world!!"}

