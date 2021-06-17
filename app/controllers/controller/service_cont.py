from uuid import UUID

from app.controllers.schemas.schemas import ServiceSchema
from app.utils.acl import (
    create_service,
    delete_service,
    get_all_service,
    get_service,
    get_service_by_name,
    update_service,
)
from core.factories import settings
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

service_router = APIRouter(prefix="/services")


# --------------- Services-----------------------


@service_router.post(
    "",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"],
)
async def add_service(data: ServiceSchema) -> JSONResponse:
    result = await create_service(data)
    return result


@service_router.get(
    "",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"],
)
async def all_services() -> JSONResponse:
    result = await get_all_service()
    return result


@service_router.get(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"],
)
async def request_service(id: UUID = Path(...)) -> JSONResponse:
    result = await get_service(id)
    return result


@service_router.get(
    "/by-name/{name}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"],
)
async def request_service_by_name(name: str = Path(...)) -> JSONResponse:
    result = await get_service_by_name(name.upper())
    return result


@service_router.put(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"],
)
async def put_service(data: ServiceSchema, id: UUID = Path(...)) -> JSONResponse:
    result = await update_service(data, id)
    return result


@service_router.delete(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["services"],
)
async def del_service(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_service(id)
    return result
