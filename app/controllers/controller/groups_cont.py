from typing import Union
from uuid import UUID

from app.controllers.schemas.schemas import GroupSchema
from app.utils.acl import (
    create_group,
    delete_group,
    get_all_group,
    get_group,
    update_group,
)
from core.factories import settings
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

group_router = APIRouter(prefix="/groups")


# --------------- Group -----------------------


@group_router.post(
    "",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"],
)
async def add_group(data: GroupSchema) -> JSONResponse:
    result = await create_group(data)
    return result


@group_router.get(
    "",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"],
)
async def request_all_groups() -> JSONResponse:
    result = await get_all_group()
    return result


@group_router.get(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"],
)
async def request_groups(id: UUID = Path(...)) -> Union[JSONResponse]:
    result = await get_group(id)
    return result


@group_router.put(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"],
)
async def put_group(data: GroupSchema, id: UUID = Path(...)) -> JSONResponse:
    result = await update_group(data, id)
    return result


@group_router.delete(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"],
)
async def del_group(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_group(id)
    return result
