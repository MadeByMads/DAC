from pydantic import BaseModel, constr, validator, ValidationError, EmailStr
from uuid import UUID   
from typing import Optional, List, Union, Mapping, Any, Dict
import pydantic.json
import asyncpg.pgproto.pgproto
from datetime import datetime


from app.controllers.controller.schemas import (
    UpdateUserSchema

)

class UserCreation(BaseModel):
    identity: str
    claim: dict = None
    created: datetime 
    updated: datetime = None
    id:  UUID 


    class Config:
        orm_mode = True



class AllUsers(UserCreation):
    ...     
    

class User(UserCreation):
    ... 
    


class ResponseSchema(BaseModel):
    result: bool = True





