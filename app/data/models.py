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
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import UniqueConstraint

#write your db models here


class Users(Model):
    __tablename__ = "users"

    identity = Column(String(),nullable=False,index=True, unique=True)
    claim = Column(JSON(),nullable=True)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)

    groups = relationship("Groups", back_populates="user")

class Groups(Model):
    __tablename__ = "groups"

    name = Column(String(),nullable=False,index=True, unique=True)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)

    user = relationship("Users", back_populates="groups")

class User_Groups(Model):
    __tablename__ = "user_groups"

    user_id = Column(UUIDType(),ForeignKey("users.id",use_alter=True, ondelete="SET NULL"),nullable=False, unique=True)
    group_id = Column(UUIDType(),ForeignKey("groups.id",use_alter=True, ondelete="SET NULL"),nullable=False)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)


class Service(Model):
    __tablename__ = "service"

    name = Column(String(), nullable=False, index=True, unique=True)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)


class Endpoint(Model):
    __tablename__ = "endpoint"
    __table_args__ = (
        UniqueConstraint("service_id", "prefix", name="uix_endpoint_service_id_prefix"),
    )

    service_id = Column(UUIDType(),ForeignKey("service.id",use_alter=True, ondelete="SET NULL"), nullable=False)
    prefix = Column(String())
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)


class Method(Model):
    __tablename__ = "method"

    name = Column(String(),nullable=False, index=True, unique=True)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)

class Permission(Model):
    __tablename__ = "permission"
    __table_args__ = (
        UniqueConstraint("entity", "entity_type", "method_id", "endpoint_id", name="uix_permission_entity_entity_type_method_id_endpoint_id"),
    )

    entity = Column(String())
    entity_type = Column(String())
    method_id = Column(UUIDType(),ForeignKey("method.id",use_alter=True, ondelete="SET NULL"),nullable=False)
    endpoint_id = Column(UUIDType(),ForeignKey("endpoint.id",use_alter=True, ondelete="SET NULL"),nullable=False)
    service_id = Column(UUIDType(),ForeignKey("service.id",use_alter=True, ondelete="SET NULL"),nullable=False)
    created = Column(Datetime(timezone=True), default=func.now())
    updated = Column(Datetime(timezone=True), onupdate=func.now(), nullable=True)
