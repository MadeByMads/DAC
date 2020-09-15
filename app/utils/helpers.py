from core.factories import settings
from datetime import datetime, timedelta
from app.data.models import TokenSessions, BlackList
from fastapi import HTTPException
from fastapi import Header
from app.controllers.controller.schemas import TokenSchema, TokenSchemaInDb
from sentry_sdk import capture_exception
from core.extensions import log
from sqlalchemy import and_
from core.extensions import db
import jwt, json,hashlib


async def get_token_header(Authorization: str = Header(...)):
    if Authorization:
        return Authorization
    raise HTTPException(status_code=401, detail="Authorization header invalid")


def extract_token(data: str) -> str:
    """ Extract JWT token from header """
    try:
        token = data.split()[1]
        return token
    except:
        return ""

def get_token_hash(token:str):
    if token and isinstance(token,str):
        return hashlib.sha256(token.encode()).hexdigest()

def clean_dict(data : dict) -> dict:
    return {key: val for (key, val) in data.items() if val is not None}


async def decode_token(token):
    try:
        return jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM]).get("identity")
    except (
        jwt.InvalidSignatureError,
        jwt.DecodeError,
        jwt.ExpiredSignatureError,
        jwt.InvalidAlgorithmError,
    ) as err:
        capture_exception(err)
        # try:
        #     identity = jwt.decode(token, verify=False)     
        #     await BlackList.create(**{"token": get_token_hash(token), "identity": str(identity)})
        #     return False
        # except:
        #     await BlackList.create(**{"token": get_token_hash(token), "identity": "unknown"})
        #     return False
        

async def create_access_token(identity: dict, expire_time: timedelta = timedelta(minutes=settings.ACCESS_TIMEDELTA)) -> str:
    """ Generate new access token for users  and save on db"""
    try:
        if identity:
            identity["exp"] = datetime.utcnow() + expire_time
            identity["type"] = "access"
            token = jwt.encode(
                identity, settings.JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM
            ).decode("utf-8")
            exp = _epoch_utc_to_datetime(identity["exp"])
            await save_token(
                token=get_token_hash(token), expire_time=exp, identity=identity.get("identity"),type=identity.get("type")
            )
            return token
    except Exception as err:
        log.error(f"Error on create_access_token function ->  {err}")
        capture_exception(err)
        return None

async def create_refresh_token(identity: dict, expire_time: timedelta = timedelta(minutes=settings.REFRESH_TIMEDELTA)) -> str:
    """ Generate new refresh token for users  and save on db"""
    try:
        if identity:
            identity["exp"] = datetime.utcnow() + expire_time
            identity["type"] = "refresh"
            token = jwt.encode(
                identity, settings.JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM
            ).decode("utf-8")
            exp = _epoch_utc_to_datetime(identity["exp"])
            await save_token(
                token=get_token_hash(token), expire_time=exp, identity=identity.get("identity"),type=identity.get("type")
            )
            return token
    except Exception as err:
        log.error(f"Error on create_refresh_token function ->  {err}")
        capture_exception(err)
        return None


async def generate_token(
    identity: dict
) -> str:
    """ Generate new access token for users  and save on db"""
    try:
        if identity:
            access = await  create_access_token(identity)
            refresh = await  create_refresh_token(identity)
            return access,refresh
    except Exception as err:
        log.error(f"Error on generate_token function ->  {err}")
        capture_exception(err)
        return None,None
    
async def recreate_access_token(
    refresh_token: str, expire_time: timedelta = timedelta(minutes=3)
) -> str:
    """ Generate new refresh token for users  and save on db"""
    try:
        identity = jwt.decode(refresh_token, settings.JWT_PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM])
     
        if identity.get("type") != "refresh":
            return None
        token = await create_access_token(identity={"identity": identity.get("identity")})
        return token
    except Exception as err:
        log.error(f"Error on recreate_access_token function ->  {err}")
        capture_exception(err)
        return None



async def check_expiration(token: str) -> bool:
    try:
        jwt.decode(
            token, settings.JWT_PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return False
    except jwt.ExpiredSignatureError:
        return True
    except Exception as err:
        log.error(f"Error on check_expiration function ->  {err}")
        return True


async def jwt_identity(token: str) -> str:
    """ decode raw data from JWT token and return identity, query result, status """
    identity, result, status = await validate_token(token)
    return (identity, result, status)


async def expire_token(token):
    identity = await  decode_token(token)
    if identity is False:
        return False
    try:

        token_info = await TokenSessions.query.where(and_(TokenSessions.identity == identity, TokenSessions.token == get_token_hash(token),TokenSessions.status == True)).gino.first()
        if token_info:
            async with db.transaction() :
                await token_info.update(status=False).apply()
                return True

        return False
    except Exception as err:
        log.error(f"Error on expire_token function ->  {err}")
        capture_exception(err)
        return False
    



async def save_token(**kwargs: dict) -> str:
    """ Save token info in  db """
   
    token_info = TokenSchema(**kwargs)
    prev_token = await TokenSessions.query.where(and_(
        TokenSessions.identity == token_info.identity,TokenSessions.type == token_info.type
    )).gino.first()
    # print(prev_token)
    async with db.transaction() :
        if prev_token is None:
            await TokenSessions.create(**token_info.dict())
        else:    
            await prev_token.update(
                token=token_info.token, expire_time=token_info.expire_time, status=True
            ).apply()
        



async def validate_token(token: str) -> tuple:
    """ Validate token signature and expire time """

    try:
        blocked_token = await BlackList.query.where(
            BlackList.token == get_token_hash(token)
        ).gino.first()
        if blocked_token is not None:
            return (None, False, False)

        identity = await decode_token(token)
        if identity is not False:
            token_in_db = await TokenSessions.query.where(
                and_(TokenSessions.identity == identity, TokenSessions.status == True)
            ).gino.first()

            if token_in_db:
                if token_in_db.token == get_token_hash(token) and identity == token_in_db.identity:
                    return (identity, True, token_in_db.status)
        return (None, False, False)
    except Exception as err:
        log.error(f"Error on validate_token function ->  {err}")
        capture_exception(err)
        return (None, False, False)


def _epoch_utc_to_datetime(token_expire):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects .
    """
    return datetime.fromtimestamp(token_expire)

