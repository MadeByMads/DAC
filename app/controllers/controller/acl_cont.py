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
from uuid import UUID
from app.controllers.controller.schemas import (
    UserSchema,
    UserSchemaDB,
    UpdateUserSchema,
   
)
from app.utils.acl import (
   create_user,
   update_user,
   delete_user,
   get_all_user,
   get_user,
)
from typing import List
from starlette.responses import JSONResponse
from starlette.requests import Request
from core.factories import settings
from typing import Union


acl_router = APIRouter()

# --------------- User -----------------------

@acl_router.post(
    "/users",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"]
)
async def add_user(data: UserSchema) -> JSONResponse:
    result = await create_user(data)
    return result

@acl_router.get(
    "/users",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"]
)
async def request_all_users() -> JSONResponse:
    result = await get_all_user()
    return result

@acl_router.get(
    "/users/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"]
)
async def request_users(id: UUID = Path(...)) -> Union[JSONResponse,UserSchemaDB]:
    result = await get_user(id)
    return result

@acl_router.put(
    "/users/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"]
)
async def put_users(data: UpdateUserSchema,id: UUID = Path(...)) -> JSONResponse:
    result = await update_user(data,id)
    return result

@acl_router.delete(
    "/users/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"]
)
async def del_users(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_user(id)
    return result










