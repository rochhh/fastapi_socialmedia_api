from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    # rating : Optional[int] = None                       # when removed Optional and only kept int , it still works


class PostCreate(PostBase):
    pass



class PostResponse(BaseModel):
    id : int
    title : str
    content : str
    published : bool
    created_at : datetime

    class Config:
        orm_mode = True

