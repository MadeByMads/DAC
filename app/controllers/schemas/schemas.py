# write your schemas in this files. Use pydantic

from pydantic import BaseModel, constr, validator, ValidationError, EmailStr
from uuid import UUID
from typing import Optional, List, Union, Mapping, Any, Dict
import pydantic.json
import asyncpg.pgproto.pgproto
from datetime import datetime

pydantic.json.ENCODERS_BY_TYPE[asyncpg.pgproto.pgproto.UUID] = str



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

    @validator("name")
    def validate_name(cls,v):
        return v.upper()

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
    name: str

    @validator("name")
    def validate_name(cls, v):
        return v.upper()

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

    @validator("name")
    def validate_name(cls,v):
        return v.upper()

class MethodSchemaDB(MethodSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True 


class PermissionSchema(BaseModel):
    entity : str
    entity_type: str
    method_id : UUID
    endpoint_id : UUID

class UpdatePermissionSchema(BaseModel):
    entity : str = None
    method_id : UUID = None
    endpoint_id : UUID = None

class PermissionSchemaDB(PermissionSchema):
    id: UUID
    created: datetime
    updated: Union[None, datetime] = None

    class Config:
        orm_mode = True 


class PermissionCheckSchema(BaseModel):
    entity: str = None
    entity_type: str = None
    service: str = None
    endpoint: str = None
    method: str = None

    @validator("method")
    def validate_method(cls,v):
        if v:
            return v.upper()
        return v

    @validator("service")
    def validate_service(cls,v):
        if v:
            return v.upper()
        return v

    @validator("entity_type")
    def validate_entity_type(cls,v):
        if v:
            return v.upper()
        return v