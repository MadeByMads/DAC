from http import HTTPStatus
from typing import List, Union
from uuid import UUID

from app.controllers.schemas.response_schema import (
    AllUsers,
    ResponseSchema,
    User,
    UserCreation,
)
from app.controllers.schemas.schemas import UpdateUserSchema, UserSchema, UserSchemaDB
from app.utils.acl import create_user, delete_user, get_all_user, get_user, update_user
from core.factories import settings
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

acl_router = APIRouter(prefix="/users")

# --------------- User -----------------------


@acl_router.post(
    "",
    response_description="Successful Response",
    description="User Creation",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"],
    summary="User Creation",
    name="User Creation",
    response_model=UserCreation,
    response_class=JSONResponse,
    status_code=HTTPStatus.OK,
)
async def add_user(data: UserSchema) -> Union[UserCreation, JSONResponse]:
    result = await create_user(data)
    return result


@acl_router.get(
    "",
    response_description="Get All Users",
    description="Get All Users",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"],
    summary="Get All Users",
    name="Get All Users",
    response_model=List[AllUsers],
    response_class=JSONResponse,
    status_code=HTTPStatus.OK,
)
async def request_all_users() -> JSONResponse:
    result = await get_all_user()
    return result


@acl_router.get(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"],
    summary="Get user by ID",
    name="Get user by ID",
    response_model=User,
    response_class=JSONResponse,
    status_code=HTTPStatus.OK,
)
async def request_users(
    id: UUID = Path(UUID, title="User ID", description="Given user ID")
) -> Union[JSONResponse, UserSchemaDB]:
    result = await get_user(id)
    return result


@acl_router.put(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"],
    summary="Update user by ID",
    name="Update user by ID",
    response_model=UpdateUserSchema,
    response_class=JSONResponse,
    status_code=HTTPStatus.OK,
)
async def put_users(
    data: UpdateUserSchema,
    id: UUID = Path(UUID, title="User ID", description="Given user ID"),
) -> JSONResponse:
    result = await update_user(data, id)
    return result


@acl_router.delete(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["users"],
    summary="Delete user by ID",
    name="Delete user by ID",
    response_model=ResponseSchema,
    response_class=JSONResponse,
    status_code=HTTPStatus.OK,
)
async def del_users(
    id: UUID = Path(UUID, title="User ID", description="Given user ID")
) -> JSONResponse:
    result = await delete_user(id)
    return result
