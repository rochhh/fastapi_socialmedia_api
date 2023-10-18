from random import randrange
from typing import Optional , List
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from .. import models , schemas , utils
from ..database import engine , get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/" , response_model=List[schemas.PostResponse])
async def get_posts( db : Session = Depends(get_db) ):

    # cursor.execute(''' SELECT * FROM posts ''')                   # sql way 
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()                             # orm way 

    return posts


@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.PostResponse)
async def create_posts( post : schemas.PostCreate ,  db : Session = Depends(get_db) ):                           # get data from the FE
    

    # cursor.execute('''                        Sql way 
                   
    #                INSERT INTO posts (title , content , published ) VALUES ( %s , %s , %s )
    #                RETURNING *
    #                ''' , 
    #                (post.title , post.content , post.published)
                   
    # )

    # new_post = cursor.fetchone()

    # conn.commit()                                                # to commit and push the data to the DB
    
                                                                    # !! IMP never directly do insert into ... values ( posts.title , posts.content ...  ) as this can lead to SQL injeciton attacks ! 


    new_post = models.Post(
        title= post.title , content= post.content , published = post.published
    )

    # alternate code for above^ models.Post( **post.dict() ) , this will add all the fields auto , instead of us adding the fields manually for eg 50 times 

    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post

        

@router.get("/{id}" , response_model=schemas.PostResponse )
async def get_post(id : int , db : Session = Depends(get_db) ):                             # id from url can be obtained as a param arg of def 
                                                                                 # response : Response is for http status codes  
    ''' 
    the id : int is done to directly add the validation to check if the id is an int or not 
    and tries to convert it to the int format as well ! 
    '''

                                                                                # the url id is a string and we have to convert it to an int for the find_post() to work 
    
    
    # cursor.execute('''
    #             SELECT * FROM posts WHERE id = %s
    #             ''' , ( str(id) )                           # if ever encounter a bug the try putting A COMMA (str(id) , )
    # )

    # post = cursor.fetchone()


    post = db.query(models.Post).filter(models.Post.id == id).first()       # .one() also works !

    if not post:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND , 
            detail= f" Id -> { id } does not exist "
                )
    
    return post

        

@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db : Session = Depends(get_db)):


    # cursor.execute('''
    #                 DELETE FROM posts WHERE id = %s RETURNING *;
    #                 ''' , 
    #                 (str(id))

    # )

    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"The id {id} does not exist ")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()


    return Response( status_code=status.HTTP_204_NO_CONTENT )



@router.put("/{id}" , response_model=schemas.PostResponse)
def update_post(id : int , post : schemas.PostCreate , db : Session = Depends(get_db) ):
    
    # cursor.execute('''
    #             UPDATE posts wh SET title = %s , content = %s , published = %s 
    #             WHERE id = %s   
    #             RETURNING *
    #                 ''' , 
    #             ( post.title , post.content , post.published , str(id), )
    # )

    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = updated_post_query.first()


    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"The id {id} does not exist ") 
    
    updated_post_query.update( post.model_dump())
    db.commit()

    return updated_post_query