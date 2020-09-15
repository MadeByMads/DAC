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
    ServiceSchema,
    ServiceSchemaDB,
)
from app.utils.acl import (
   create_service,
   update_service,
   delete_service,
   get_all_service,
   get_service
)
from typing import List
from starlette.responses import JSONResponse
from app.utils.helpers import clean_dict
from app.data.models import TokenSessions
from starlette.requests import Request
from core.factories import settings
from typing import Union


service_router = APIRouter()



# --------------- Services-----------------------



@service_router.post(
    "/services",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"]
)
async def add_service(data: ServiceSchema) -> JSONResponse:
    result = await create_service(data)
    return result

@service_router.get(
    "/services",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"]
)
async def all_services() -> JSONResponse:
    result = await get_all_service()
    return result

@service_router.get(
    "/services/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"]
)
async def request_service(id: UUID = Path(...)) ->JSONResponse:
    result = await get_service(id)
    return result

@service_router.put(
    "/services/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"]
)
async def put_service(data: ServiceSchema ,id: UUID = Path(...)) -> JSONResponse:
    result = await update_service(data,id)
    return result

@service_router.delete(
    "/services/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"]
)
async def del_service(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_service(id)
    return result
