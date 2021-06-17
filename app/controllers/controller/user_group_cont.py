from typing import Union
from uuid import UUID

from app.controllers.schemas.schemas import (
    UpdateUserGroupSchema,
    UserGroupSchema,
    UserGroupSchemaDB,
)
from app.utils.acl import (
    create_us_gr,
    delete_us_gr,
    get_all_us_gr,
    get_us_gr,
    update_us_gr,
)
from core.factories import settings
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

us_gr_router = APIRouter(prefix="/user-groups")


# --------------- User - Group -----------------------


@us_gr_router.post(
    "",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["user-groups"],
)
async def add_user_group(data: UserGroupSchema) -> JSONResponse:
    result = await create_us_gr(data)
    return result


@us_gr_router.get(
    "",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["user-groups"],
)
async def all_user_groups() -> JSONResponse:
    result = await get_all_us_gr()
    return result


@us_gr_router.get(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["user-groups"],
)
async def request_user_groups(
    id: UUID = Path(...),
) -> Union[JSONResponse, UserGroupSchemaDB]:
    result = await get_us_gr(id)
    return result


@us_gr_router.put(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["user-groups"],
)
async def put_user_group(
    data: UpdateUserGroupSchema, id: UUID = Path(...)
) -> JSONResponse:
    result = await update_us_gr(data, id)
    return result


@us_gr_router.delete(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["user-groups"],
)
async def del_user_group(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_us_gr(id)
    return result
