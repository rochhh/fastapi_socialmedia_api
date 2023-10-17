from random import randrange
from typing import Optional
from fastapi import FastAPI 
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
async def root():
    return {"data_to_fe": my_posts}


@app.post("/posts")
async def root( payload : Post  ):                           # get data from the FE
    
    post_dict = payload.model_dump()                         
    post_dict["id"] = randrange(0,1000000)
    
    my_posts.append(post_dict)



    return {"message": f" the req was sent to the BE ! , {post_dict}" }


