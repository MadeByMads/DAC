from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.extensions import db


class SurrogatePK:
    """A mixin that adds a surrogate UUID 'primary key' column named ``id`` to
    any declarative-mapped class."""

    __table_args__ = {"extend_existing": True}

    id = db.Column(UUID(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=True)


class Model(SurrogatePK, db.Model):
    __abstract__ = True

    @classmethod
    def exists(cls, ent_id):
        result = cls.query.get(ent_id)
        return result is not None

    @classmethod
    async def create(cls, **kwargs):
        if issubclass(cls, SurrogatePK):
            print(kwargs)
            unique_id = uuid4()
            if not kwargs.get("id"):

                kwargs["id"] = unique_id
        return await cls(**kwargs)._create()
