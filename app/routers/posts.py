from typing import List, Optional

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, oauth2
from app.database import get_db
from execeptions.DataNotFoundException import DataNotFoundException

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


def _and(param):
    pass


@router.get("/", response_model=List[schemas.Post])
def get_posts(limit: int = 10, skip: int = 0, search:Optional[str]="", db: Session = Depends(get_db),
              current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # above db is injected as a dependency
    # using pydantic (Similar to hibernate/Spring Data where as sqlalchemy is similar to JPA
    # cursor.execute("""SELECT * FROM POSTS""")
    # posts = cursor.fetchall()
    print(limit)
    print(search)
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    # return {"data": posts}
    return posts


@router.get("/{id}", response_model=schemas.Post)
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


@router.post("/", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    try:
        # cursor.execute("""INSERT INTO POSTS(TITLE,CONTENT) VALUES (%s,%s) RETURNING * """, (post.title, post.content))
        # new_post = cursor.fetchone()
        # conn.commit()
        print(current_user.password)
        # new_post = models.Post(title=post.title,content=post.content,published=post.published)
        new_post = models.Post(owner_id=current_user.id, **post.dict())
        # print(type(new_post))
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="internal Server Error")


@router.delete("/{id}", status_code=204)
def delete_post(id, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    try:
        try:
            id = int(id)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid ID format. Please provide an integer.")
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()
        if post is None:
            raise DataNotFoundException(f"Post with id: {id} Not Found!")
        if post.owner_id != current_user.id:
            raise HTTPException(status_code=403,
                                detail=f"User with {current_user.id} not authorized to perform requested action")
        post_query.delete(synchronize_session=False)
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
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}", status_code=200, response_model=schemas.Post)
def update_posts(id, post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    try:
        try:
            id = int(id)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid ID format. Please provide an integer.")
        post_query = db.query(models.Post).filter(models.Post.id == id)
        filtered_post = post_query.first()
        if filtered_post is None:
            raise DataNotFoundException(f"Post with id: {id} Not Found!")
        # post_query.update({'title':'hey updated title', 'content':'Updated content'}, synchronize_session=False)
        if filtered_post.owner_id != current_user.id:
            raise HTTPException(status_code=403,
                                detail=f"User with {current_user.id} not authorized to perform requested action")
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
