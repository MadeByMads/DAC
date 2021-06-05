from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class UserCreation(BaseModel):
    id: UUID
    identity: str
    claim: Optional[Dict[str, Any]]
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class AllUsers(UserCreation):
    ...


class User(UserCreation):
    ...


class ResponseSchema(BaseModel):
    result: bool = True
