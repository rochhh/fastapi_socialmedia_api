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
     prefix="/users",
     tags=['Users']
)



@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.UserOutput )
async def create_user(  user_data : schemas.UserCreate , db : Session = Depends(get_db) ):


    # ! hashing password !

    hashed_password = utils.hash_password(user_data.password)
    user_data.password = hashed_password

    create_user = models.User(
        **user_data.model_dump()
    )

    db.add(create_user)
    db.commit()
    db.refresh(create_user)


    return create_user


@router.get("/{id}" , status_code=status.HTTP_200_OK , response_model=schemas.UserOutput  )
async def get_user( id : int , db : Session = Depends(get_db) ):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND , 
            detail= f" Id -> { id } does not exist "
                )

    return user