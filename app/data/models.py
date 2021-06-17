from app.controllers.schemas.schemas import USER_TYPES
from core.dbsetup import Model, db
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, JSON, UUID
from sqlalchemy.orm import relationship


class Users(Model):
    __tablename__ = "users"

    identity = db.Column(db.String(), nullable=False, index=True, unique=True)
    claim = db.Column(JSON(), nullable=True)

    groups = relationship("Groups", back_populates="user")


class Groups(Model):
    __tablename__ = "groups"

    name = db.Column(ENUM(USER_TYPES), nullable=False, index=True, unique=True)

    user = relationship("Users", back_populates="groups")


class User_Groups(Model):
    __tablename__ = "user_groups"

    user_id = db.Column(
        UUID(),
        ForeignKey("users.id", use_alter=True, ondelete="SET NULL"),
        nullable=False,
        unique=True,
    )
    group_id = db.Column(
        UUID(),
        ForeignKey("groups.id", use_alter=True, ondelete="SET NULL"),
        nullable=False,
    )


class Service(Model):
    __tablename__ = "service"

    name = db.Column(db.String(), nullable=False, index=True, unique=True)


class Endpoint(Model):
    __tablename__ = "endpoint"
    __table_args__ = (
        UniqueConstraint("service_id", "prefix", name="uix_endpoint_service_id_prefix"),
    )

    service_id = db.Column(
        UUID(),
        ForeignKey("service.id", use_alter=True, ondelete="SET NULL"),
        nullable=False,
    )
    prefix = db.Column(db.String())


class Method(Model):
    __tablename__ = "method"

    name = db.Column(db.String(), nullable=False, index=True, unique=True)


class Permission(Model):
    __tablename__ = "permission"
    __table_args__ = (
        UniqueConstraint(
            "entity",
            "entity_type",
            "method_id",
            "endpoint_id",
            name="uix_permission_entity_entity_type_method_id_endpoint_id",
        ),
    )

    entity = db.Column(db.String())
    entity_type = db.Column(db.String())
    method_id = db.Column(
        UUID(),
        ForeignKey("method.id", use_alter=True, ondelete="SET NULL"),
        nullable=False,
    )
    endpoint_id = db.Column(
        UUID(),
        ForeignKey("endpoint.id", use_alter=True, ondelete="SET NULL"),
        nullable=False,
    )
    service_id = db.Column(
        UUID(),
        ForeignKey("service.id", use_alter=True, ondelete="SET NULL"),
        nullable=False,
    )


class TokenSessions(Model):
    __tablename__ = "token_session"

    iss = db.Column(db.String(), unique=True, nullable=False)
    exp = db.Column(db.DateTime(timezone=True), nullable=False)
    identity = db.Column(db.String(), nullable=False, index=True)
    type = db.Column(db.String(), nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default=True)
    iat = db.Column(db.DateTime(timezone=True), nullable=False)
    role = db.Column(db.String(), nullable=False)
