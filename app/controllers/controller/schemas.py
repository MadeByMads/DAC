# write your schemas in this files. Use pydantic

from pydantic import BaseModel,constr,validator,ValidationError,EmailStr
from uuid import UUID
from typing import Optional,List,Union,Dict,Any
import pydantic.json
from datetime import datetime
import asyncpg.pgproto.pgproto
pydantic.json.ENCODERS_BY_TYPE[asyncpg.pgproto.pgproto.UUID] = str


# Write your pydantic models here

class TestSchema(BaseModel):
    test: str 
    status_code: int
    class Config:
        schema_extra = {
             'example': {
                'test': "Test",
                "status_code": 200
              
            }
        }

class TestErrorSchema(BaseModel):
    test: str 
    status_code: int
    class Config:
        schema_extra = {
             'example': {
                'test': "Test Error",
                "status_code": 404
              
            }
        }


class UserSchema(BaseModel):
    identity: str
    claim : Dict[Any, Any] = None


class UserSchemaDB(UserSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True

class GroupSchema(BaseModel):
    name: str


class GroupSchemaDB(GroupSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True

class UserGroupSchema(BaseModel):
    user_id: UUID
    group_id : UUID

class UserGroupSchemaDB(UserGroupSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True

class ServiceSchema(BaseModel):
    name : str

class ServiceSchemaDB(ServiceSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True 


class EndpointSchema(BaseModel):
    service_id : UUID
    prefix: str = None

class EndpointSchemaDB(EndpointSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True 


class MethodSchema(BaseModel):
    name: str

class MethodSchemaDB(MethodSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True 


class PermissionSchema(BaseModel):
    endtity : str
    method_id : UUID
    endpoint_id : UUID

class PermissionSchemaDB(PermissionSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True 
