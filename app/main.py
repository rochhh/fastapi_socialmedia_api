from random import randrange
from typing import Optional
from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    # rating : Optional[int] = None                       # when removed Optional and only kept int , it still works


while True:                                             # keep looping under connection is established , or the app wont start 

    try :
        conn = psycopg2.connect(
            host="localhost" , <credentials> , cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("db conn success")
        break

    except Exception as e:
        print(e)
        time.sleep(2)


my_posts = [
    {"id": 1 , "title": "title_1" , "content": "content_1"},
    {"id": 2 , "title": "title_2" , "content": "content_2"},
]

@app.get("/posts")
async def get_posts():

    cursor.execute(''' SELECT * FROM posts ''')
    posts = cursor.fetchall()

    return {"data_to_fe": posts}


@app.post("/posts" , status_code=status.HTTP_201_CREATED)
async def create_posts( post : Post ):                           # get data from the FE
    

    cursor.execute('''
                   
                   INSERT INTO posts (title , content , published ) VALUES ( %s , %s , %s )
                   RETURNING *
                   ''' , 
                   (post.title , post.content , post.published)
                   
    )

    new_post = cursor.fetchone()

    conn.commit()                                                # to commit and push the data to the DB
    
                                                                    # !! IMP never directly do insert into ... values ( posts.title , posts.content ...  ) as this can lead to SQL injeciton attacks ! 


    return {"message": f" the req was sent to the BE ! , {new_post}" }



def find_post(id):

    for post in my_posts:
        if post["id"] == id:
            return post
        


@app.get("/posts/{id}")
async def get_post(id : int ):                             # id from url can be obtained as a param arg of def 
                                                                                 # response : Response is for http status codes  
    ''' 
    the id : int is done to directly add the validation to check if the id is an int or not 
    and tries to convert it to the int format as well ! 
    '''

                                                                                # the url id is a string and we have to convert it to an int for the find_post() to work 
    
    
    cursor.execute('''
                SELECT * FROM posts WHERE id = %s
                ''' , ( str(id) )                           # if ever encounter a bug the try putting A COMMA (str(id) , )
    )

    post = cursor.fetchone()

    if not post:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND , 
            detail= f" Id -> { id } does not exist "
                )
    
    return {"message" : f"the post id is -> { post }"}



def find_index_post(id):

    for idx , post in enumerate(my_posts):

        if post["id"] == id:
            return idx
        


@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):


    cursor.execute('''
                    DELETE FROM posts WHERE id = %s RETURNING *;
                    ''' , 
                    (str(id))

    )

    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"The id {id} does not exist ")
    
    return Response( status_code=status.HTTP_204_NO_CONTENT )



@app.put("/posts/{id}")
def update_post(id : int , post : Post ):
    
    cursor.execute('''
                UPDATE posts wh SET title = %s , content = %s , published = %s 
                WHERE id = %s   
                RETURNING *
                    ''' , 
                ( post.title , post.content , post.published , str(id), )
    )

    updated_post = cursor.fetchone()
    conn.commit()


    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"The id {id} does not exist ") 
    
    return {"data": updated_post}

