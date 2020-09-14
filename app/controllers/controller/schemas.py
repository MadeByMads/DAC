# write your schemas in this files. Use pydantic

from pydantic import BaseModel,constr,validator,ValidationError,EmailStr
from uuid import UUID
from typing import Optional,List,Union,Dict,Any
import pydantic.json
from datetime import datetime
import asyncpg.pgproto.pgproto
pydantic.json.ENCODERS_BY_TYPE[asyncpg.pgproto.pgproto.UUID] = str


# Write your pydantic models here



class UserSchema(BaseModel):
    identity: str
    claim : Dict[Any, Any] = None

class UpdateUserSchema(BaseModel):
    identity: str = None
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


class UpdateUserGroupSchema(BaseModel):
    user_id: UUID = None
    group_id : UUID = None
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

class UpdateEndpointSchema(BaseModel):
    service_id : UUID = None
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

class UpdatePermissionSchema(BaseModel):
    endtity : str = None
    method_id : UUID = None
    endpoint_id : UUID = None

class PermissionSchemaDB(PermissionSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True 
