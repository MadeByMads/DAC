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
    GroupSchema,
    GroupSchemaDB,
   
)
from app.utils.acl import (
   create_group, 
   update_group,
   delete_group,
   get_all_group,
   get_group,
)
from typing import List
from starlette.responses import JSONResponse
from app.utils.helpers import clean_dict
from starlette.requests import Request
from core.factories import settings
from typing import Union


group_router = APIRouter()



# --------------- Group -----------------------


@group_router.post(
    "/groups",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"]
)
async def add_group(data: GroupSchema) -> JSONResponse:
    result = await create_group(data)
    return result

@group_router.get(
    "/groups",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"]
)
async def request_all_groups() -> JSONResponse:
    result = await get_all_group()
    return result

@group_router.get(
    "/groups/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"]
)
async def request_groups(id: UUID = Path(...)) -> Union[JSONResponse]:
    result = await get_group(id)
    return result

@group_router.put(
    "/groups/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"]
)
async def put_group(data: GroupSchema ,id: UUID = Path(...)) -> JSONResponse:
    result = await update_group(data,id)
    return result

@group_router.delete(
    "/groups/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["groups"]
)
async def del_group(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_group(id)
    return result
