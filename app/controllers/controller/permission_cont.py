from uuid import UUID

from app.controllers.schemas.schemas import (
    PermissionSchema,
    PermissionSchemaDB,
    UpdatePermissionSchema,
)
from app.utils.acl import (
    create_permission,
    delete_permission,
    get_all_permissions,
    get_permission,
    update_permission,
)
from core.factories import settings
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

permission_router = APIRouter(prefix="/permissions")

# --------------- User -----------------------


@permission_router.post(
    "",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"],
)
async def add_permission(data: PermissionSchema) -> JSONResponse:
    result = await create_permission(data)
    return result


@permission_router.get(
    "",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"],
)
async def request_all_permissions() -> JSONResponse:
    result = await get_all_permissions()
    return result


@permission_router.get(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"],
)
async def request_permission(id: UUID = Path(...)) -> JSONResponse:
    result = await get_permission(id)
    return result


@permission_router.put(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"],
)
async def put_permission(
    data: UpdatePermissionSchema, id: UUID = Path(...)
) -> JSONResponse:
    result = await update_permission(data, id)
    return result


@permission_router.delete(
    "/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"],
)
async def del_users(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_permission(id)
    return result
