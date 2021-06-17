from datetime import datetime, timedelta

from app.controllers.schemas.schemas import JWTHeaders, JWTPayload
from app.data.models import TokenSessions
from authlib.jose import jwt
from core.extensions import db
from core.factories import settings


class JWTOperations:
    def __init__(self, header=None):
        self.jwt_header = header or JWTHeaders().dict()

    async def jwt_encode(self, identity: str):
        payload = JWTPayload(
            **{
                "exp": datetime.now() + timedelta(settings.JWT_ACCESS_TIMEDELTA),
                "identity": identity,
            }
        )
        token = jwt.encode(
            header=self.jwt_header, payload=payload.dict(), key=settings.JWT_PRIVATE_KEY
        )
        async with db.transaction():
            await TokenSessions.create(**payload)

        return token
