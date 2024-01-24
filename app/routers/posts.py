from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from execeptions.DataNotFoundException import DataNotFoundException

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # above db is injected as a dependency
    # using pydantic (Similar to hibernate/Spring Data where as sqlalchemy is similar to JPA
    # cursor.execute("""SELECT * FROM POSTS""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    # return {"data": posts}
    return posts


@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id, db: Session = Depends(get_db)):
    try:
        try:
            id = int(id)
        except:
            raise ValueError("Parsing error!")
        post = db.query(models.Post).filter(models.Post.id == id).first()
        print("post ", post)
        if post is None:
            raise DataNotFoundException(f"Post with id: {id} Not Found!")
        # return JSONResponse(content={"data": post}, status_code=200)
        return post
        # next((i for i in my_p
        # osts if i['id'] == post_id), None)
        # for i in my_posts:
        #     if i['id'] == int(id):
        #         return JSONResponse(content={"data": i}, status_code=200)
        # raise DataNotFoundException(f"Post with id: {id} Not Found!")
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid ID format. Please provide an integer.")
    except DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print("inside service exception", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/posts", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        # cursor.execute("""INSERT INTO POSTS(TITLE,CONTENT) VALUES (%s,%s) RETURNING * """, (post.title, post.content))
        # new_post = cursor.fetchone()
        # conn.commit()

        # new_post = models.Post(title=post.title,content=post.content,published=post.published)
        new_post = models.Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="internal Server Error")


@router.delete("/posts/{id}", status_code=204)
def delete_post(id, db: Session = Depends(get_db)):
    try:
        try:
            id = int(id)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid ID format. Please provide an integer.")
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if post is None:
            raise DataNotFoundException(f"Post with id: {id} Not Found!")
        post.delete(synchronize_session=False)
        db.commit()

        # updated_posts = [i for i in my_posts if i['id'] != id]
        # print(updated_posts)
        # print(type(updated_posts))
        # if len(updated_posts) != len(my_posts):
        #     my_posts.clear()
        #     my_posts.extend(updated_posts)
        #     print(my_posts)
        #     # return JSONResponse(content=None, status_code=204)
        # else:
        #     raise DataNotFoundException(f"Post with id: {id} Not Found!")
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid ID format. Please provide an integer.")
    except DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/posts/{id}", status_code=200, response_model=schemas.Post)
def update_posts(id, post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        try:
            id = int(id)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid ID format. Please provide an integer.")
        post_query = db.query(models.Post).filter(models.Post.id == id)
        if post_query.first() is None:
            raise DataNotFoundException(f"Post with id: {id} Not Found!")
        # post_query.update({'title':'hey updated title', 'content':'Updated content'}, synchronize_session=False)
        post_query.update(post.dict(), synchronize_session=False)

        db.commit()

        # cursor.execute("""SELECT * FROM POSTS where id= (%s)""", str(id))
        # db_post = cursor.fetchone()
        # if db_post is None:
        #     raise DataNotFoundException(f"Post with id: {id} Not Found!")
        #
        # # updated_post = db_post.copy()
        # updated_fields = {}
        # print(updated_fields)
        # print(post.title)
        # if post.title:
        #     updated_fields['title'] = post.title
        # if post.content:
        #     updated_fields['content'] = post.content
        # if post.published:
        #     updated_fields['published'] = post.published
        # print(updated_fields)
        # update_query = "UPDATE POSTS SET " + ", ".join(f"{field} = %s" for field in updated_fields.keys())
        # update_query += " WHERE id = %s RETURNING *"
        # query_parameters = list(updated_fields.values()) + [str(id)]
        #
        # # Print the constructed query and parameters (for debugging)
        # print("Dynamic Query:", update_query)
        # print("Parameters:", query_parameters)
        #
        # # Execute the dynamic query
        # cursor.execute(update_query, query_parameters)
        # updated_post = cursor.fetchone()
        # conn.commit()
        # my_posts[post_index] = updated_post
        # print(my_posts)
        # return JSONResponse(content={"data": updated_post}, status_code=200)
        # return {"data": post_query.first()}
        return post_query.first()
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid ID format. Please provide an integer.")
    except DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
