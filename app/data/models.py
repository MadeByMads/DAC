from core.dbsetup import (
    Column,
    Model,
    UUIDType,
    relationship,
    String,
    Integer,
    ForeignKey,
    BOOLEAN,
    Datetime,
    Date,
    Text
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON, ENUM

from enum import Enum as PyEnum
#write your db models here

class EntityEnum(PyEnum):
    user = 1
    group = 2
    service = 3


class TokenSessions(Model):
    __tablename__ = "token_session"

    token = Column(String(), unique=True, nullable=False)
    expire_time = Column(Datetime(timezone=True), nullable=False)
    identity = Column(String(), nullable=False, index=True)
    type = Column(String(),nullable=True)
    status = Column(BOOLEAN(), nullable=False, default=True)


class BlackList(Model):
    __tablename__ = "black_list"

    token = Column(String(), nullable=False)
    identity = Column(String(), nullable=True)

class Users(Model):
    __tablename__ = "users"

    identity = Column(String(),nullable=False,index=True)
    claim = Column(JSON(),nullable=True)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)


class Groups(Model):
    __tablename__ = "groups"

    name = Column(String(),nullable=False,index=True)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)


class User_Groups(Model):
    __tablename__ = "user_groups"

    user_id = Column(UUIDType(),ForeignKey("users.id",use_alter=True, ondelete="SET NULL"),nullable=False)
    group_id = Column(UUIDType(),ForeignKey("groups.id",use_alter=True, ondelete="SET NULL"),nullable=False)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)


class Service(Model):
    __tablename__ = "service"

    name = Column(String(),nullable=False, index=True)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)


class Endpoint(Model):
    __tablename__ = "endpoint"

    service_id = Column(UUIDType(),ForeignKey("service.id",use_alter=True, ondelete="SET NULL"),nullable=False)
    prefix = Column(String())
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)


class Method(Model):
    __tablename__ = "method"

    name = Column(String(),nullable=False, index=True)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)

class Permission(Model):
    __tablename__ = "permission"
    
    entity = Column(String())
    entity_type = Column(ENUM(EntityEnum), use_alter=True)

    method_id = Column(UUIDType(),ForeignKey("method.id",use_alter=True, ondelete="SET NULL"),nullable=False)
    endpoint_id = Column(UUIDType(),ForeignKey("endpoint.id",use_alter=True, ondelete="SET NULL"),nullable=False)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)



