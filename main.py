from random import randrange
from typing import Optional
from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None                       # when removed Optional and only kept int , it still works



my_posts = [
    {"id": 1 , "title": "title_1" , "content": "content_1"},
    {"id": 2 , "title": "title_2" , "content": "content_2"},
]

@app.get("/posts")
async def get_posts():
    return {"data_to_fe": my_posts}


@app.post("/posts" , status_code=status.HTTP_201_CREATED)
async def create_posts( payload : Post  ):                           # get data from the FE
    
    post_dict = payload.model_dump()                         
    post_dict["id"] = randrange(0,1000000)
    
    my_posts.append(post_dict)

    return {"message": f" the req was sent to the BE ! , {post_dict}" }



def find_post(id):

    for post in my_posts:
        if post["id"] == id:
            return post
        


@app.get("/posts/{id}")
async def get_post(id : int , response : Response ):                             # id from url can be obtained as a param arg of def 
                                                                                 # response : Response is for http status codes  
    ''' 
    the id : int is done to directly add the validation to check if the id is an int or not 
    and tries to convert it to the int format as well ! 
    '''

                                                                                # the url id is a string and we have to convert it to an int for the find_post() to work 
    
    post = find_post(id)

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND 
        # return {"message": f" Id -> { id } does not exist "}

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
     
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"The id {id} does not exist ")
    
    my_posts.pop(index)

    return Response( status_code=status.HTTP_204_NO_CONTENT )



@app.put("/posts/{id}")
def update_post(id : int , post : Post ):
    
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"The id {id} does not exist ") 
    
    # for idx , post in enumerate(my_posts):

    #     if post["id"] == id:

    #         post[idx] = post

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post

    return {"data": post_dict}

