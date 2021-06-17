# write your schemas in this files. Use pydantic

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

import asyncpg.pgproto.pgproto
import pydantic.json
from app.data.models import USER_TYPES
from core.factories import settings
from pydantic import BaseModel, validator

pydantic.json.ENCODERS_BY_TYPE[asyncpg.pgproto.pgproto.UUID] = str


class UserSchema(BaseModel):
    identity: str
    claim: Optional[Dict[Any, Any]]


class UpdateUserSchema(BaseModel):
    identity: Optional[str]
    claim: Optional[Dict[Any, Any]]


class UserSchemaDB(UserSchema):
    id: UUID
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class GroupSchema(BaseModel):
    name: USER_TYPES

    class Config:
        use_enum_values = True

    @validator("name")
    def validate_name(cls, v):
        return v.upper()


class GroupSchemaDB(GroupSchema):
    id: UUID
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class UserGroupSchema(BaseModel):
    user_id: UUID
    group_id: UUID


class UpdateUserGroupSchema(BaseModel):
    user_id: Optional[UUID]
    group_id: Optional[UUID]


class UserGroupSchemaDB(UserGroupSchema):
    id: UUID
    created: datetime
    updated: Optional[datetime]

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
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class EndpointSchema(BaseModel):
    service_id: UUID
    prefix: Optional[str]


class UpdateEndpointSchema(BaseModel):
    service_id: Optional[UUID]
    prefix: Optional[str]


class EndpointSchemaDB(EndpointSchema):
    id: UUID
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class MethodSchema(BaseModel):
    name: str

    @validator("name")
    def validate_name(cls, v):
        return v.upper()


class MethodSchemaDB(MethodSchema):
    id: UUID
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class PermissionSchema(BaseModel):
    entity: str
    entity_type: str
    service_id: UUID
    method_id: UUID
    endpoint_id: UUID


class UpdatePermissionSchema(BaseModel):
    entity: Optional[str]
    method_id: Optional[UUID]
    endpoint_id: Optional[UUID]


class PermissionSchemaDB(PermissionSchema):
    id: UUID
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class PermissionCheckSchema(BaseModel):
    entity: Optional[str]
    entity_type: Optional[str]
    service: Optional[str]
    endpoint: Optional[str]
    method: Optional[str]

    @validator("method", "entity_type", "service")
    def _upper(cls, v):
        if v:
            return v.upper()
        return v


class JWTPayload(BaseModel):
    iss: str = settings.JWT_ISSUER
    iat: datetime = datetime.now()
    exp: datetime
    identity: str
    role: str
    type: str = "ACCESS"


class JWTHeaders(BaseModel):
    alg: str = "RS256"
    typ: str = "JWT"
