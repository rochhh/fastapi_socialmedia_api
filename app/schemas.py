from datetime import datetime
from pydantic import BaseModel , EmailStr
from datetime import datetime

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


class UserCreate(BaseModel):
    
    email : EmailStr
    password : str 


class UserOutput(BaseModel):

    id : int
    email : EmailStr
    created_at : datetime

    class Config :                                                              # done for only making sure a specific data is only viewed by the FE 
        orm_mode = True 

