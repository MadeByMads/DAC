from fastapi import (
    APIRouter,
    HTTPException,
    Cookie,
    Depends,
    Header,
    File,
    Body,
    Path,
    Query,
)
from app.controllers.controller.schemas import TokenResponseSchema
from uuid import UUID
from app.utils.helpers import (
    generate_token,
    extract_token,
    validate_token,
    jwt_identity,
    check_expiration,
    expire_token,
    create_access_token,
    extract_token,
    recreate_access_token,
    get_token_header
)
from typing import List
from starlette.responses import JSONResponse
from app.utils.helpers import clean_dict
from app.data.models import TokenSessions
from starlette.requests import Request
from core.factories import settings
from datetime import timedelta

router = APIRouter()


@router.post(
    "/generator/default",
    response_description="Create default token",
    description="",
    response_model=TokenResponseSchema,
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["Token"]
)
async def create_token(identity: dict = Body(...,example={"identity" : "your_identity"})) -> JSONResponse:

    access,refresh = await generate_token(identity)
    print("TOKEEEN " ,access)
    return (
        JSONResponse(content={"token": access, "refresh": refresh, "result": True}, status_code=200)
        if access
        else JSONResponse(content={"token": "","result" : False}, status_code=404)
    )

@router.post(
    "/generator/refresh",
    response_description="Create default token",
    description="",
    response_model=TokenResponseSchema,
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["Token"]
)
async def refresh_token(Authorization: str =Header(...)) -> JSONResponse:
    token = extract_token(Authorization)
    print( token)
    token = await recreate_access_token(token)
    print("TOKEEEN " ,token)
    return (
        JSONResponse(content={"token": token, "result": True}, status_code=200)
        if token
        else JSONResponse(content={"token": "","result" : False}, status_code=401)
    )


@router.delete(
    "/generator/expire",
    response_description="Expire tokens",
    description="",
    response_model=TokenResponseSchema,
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["Token"]
)
async def expire_token_generator(Authorization: str = Header(...)) -> JSONResponse:
    token = extract_token(Authorization)
    result = await expire_token(token)

    return (
        JSONResponse(content={"result": result}, status_code=200)
        if result
        else JSONResponse(content={"result" : result}, status_code=404)
    )

@router.get(
    "/generator/identity",
    response_description="Get user identity if token is valid",
    description="Extract identity from token ",
    response_model=TokenResponseSchema,
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["Token"]
)
async def get_identity(
    token: str = Query(None),
    Authorization: str = Header(None)
) -> JSONResponse:

    if token:
        identity, result, status = await jwt_identity(token)
    else:
        token = extract_token(Authorization)
        identity, result, status = await jwt_identity(token)
        expire = await check_expiration(token) 

    return (
        JSONResponse(
            {
                "result": result,
                "identity": identity,
                "status": status,
                "message": "Success",
                "expire" : expire
            },
            status_code=200,
        )
        if result
        else JSONResponse(
            {
                "result": result,
                "identity": identity,
                "status": status,
                "expire" : True,
                "message": "Not Found",
            },
            status_code=404,
        )
    )


@router.get(
    "/generator/check",
    response_description="validate token",
    description="Validate token signature provided on header",
    response_model=TokenResponseSchema,
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["Token"]
)
async def check_token(
    Authorization: str = Header(None), token=Query(None)
) -> JSONResponse:

    if Authorization:
        token = extract_token(Authorization)
        identity, result, _ = await validate_token(token)
    else:
        identity, result, _ = await validate_token(token)
    return (
        JSONResponse(content={"error": "Token validation error","result": result, "identity": identity}, status_code=401)
        if not result
        else JSONResponse(
            content={"result": result, "identity": identity}, status_code=200
        )
    )

