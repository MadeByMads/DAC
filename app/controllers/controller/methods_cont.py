from uuid import UUID

from app.controllers.schemas.schemas import MethodSchema
from app.utils.acl import (
    create_method,
    delete_method,
    get_all_method,
    get_method,
    get_method_by_name,
    update_method,
)
from core.factories import settings
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

method_router = APIRouter()

# --------------- User -----------------------


@method_router.post(
    "/methods",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"],
)
async def add_method(data: MethodSchema) -> JSONResponse:
    result = await create_method(data)
    return result


@method_router.get(
    "/methods",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"],
)
async def request_all_methods() -> JSONResponse:
    result = await get_all_method()
    return result


@method_router.get(
    "/methods/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"],
)
async def request_method(id: UUID = Path(...)) -> JSONResponse:
    result = await get_method(id)
    return result


@method_router.put(
    "/methods/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"],
)
async def put_method(data: MethodSchema, id: UUID = Path(...)) -> JSONResponse:
    result = await update_method(data, id)
    return result


@method_router.delete(
    "/methods/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["methods"],
)
async def del_method(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_method(id)
    return result
