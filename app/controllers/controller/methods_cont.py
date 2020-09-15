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
    MethodSchema,
    MethodSchemaDB,
)
from app.utils.acl import (
   create_method,
   update_method,
   delete_method,
   get_all_method,
   get_method,
)
from typing import List
from starlette.responses import JSONResponse
from starlette.requests import Request
from core.factories import settings
from typing import Union


method_router = APIRouter()

# --------------- User -----------------------

@method_router.post(
    "/methods",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"]
)
async def add_method(data: MethodSchema) -> JSONResponse:
    result = await create_method(data)
    return result

@method_router.get(
    "/methods",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"]
)
async def request_all_methods() -> JSONResponse:
    result = await get_all_method()
    return result

@method_router.get(
    "/methods/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"]
)
async def request_method(id: UUID = Path(...)) ->JSONResponse:
    result = await get_method(id)
    return result

@method_router.put(
    "/methods/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"]
)
async def put_method(data: MethodSchema,id: UUID = Path(...)) -> JSONResponse:
    result = await update_method(data,id)
    return result

@method_router.delete(
    "/methods/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"]
)
async def del_method(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_method(id)
    return result










