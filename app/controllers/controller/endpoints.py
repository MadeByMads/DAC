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
from app.controllers.schemas.schemas import (
    EndpointSchema,
    EndpointSchemaDB,
)
from app.utils.acl import (
   create_endpoint,
   update_endpoint,
   delete_endpoint,
   get_all_endpoints,
   get_endpoint,
   get_endpoint_by_name,
)
from typing import List
from starlette.responses import JSONResponse
from starlette.requests import Request
from core.factories import settings
from typing import Union


endpoint_router = APIRouter()

# --------------- User -----------------------

@endpoint_router.post(
    "/endpoints",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["endpoints"]
)
async def add_method(data: EndpointSchema) -> JSONResponse:
    result = await create_endpoint(data)
    return result

@endpoint_router.get(
    "/endpoints",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["endpoints"]
)
async def request_all_methods() -> JSONResponse:
    result = await get_all_endpoints()
    return result

@endpoint_router.get(
    "/endpoints/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["endpoints"]
)
async def request_method(id: UUID = Path(...)) ->JSONResponse:
    result = await get_endpoint(id)
    return result

@endpoint_router.put(
    "/endpoints/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["endpoints"]
)
async def put_method(data: EndpointSchema, id: UUID = Path(...)) -> JSONResponse:
    result = await update_endpoint(data, id)
    return result

@endpoint_router.delete(
    "/endpoints/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["endpoints"]
)
async def del_method(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_endpoint(id)
    return result






