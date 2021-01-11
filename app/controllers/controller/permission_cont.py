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
   PermissionSchema,
   PermissionSchemaDB,
   UpdatePermissionSchema
)
from app.utils.acl import (
   create_permission,
   update_permission,
   delete_permission,
   get_all_permissions,
   get_permission,
)
from typing import List
from starlette.responses import JSONResponse
from starlette.requests import Request
from core.factories import settings
from typing import Union


permission_router = APIRouter()

# --------------- User -----------------------

@permission_router.post(
    "/permissions",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"]
)
async def add_permission(data: PermissionSchema) -> JSONResponse:
    result = await create_permission(data)
    return result

@permission_router.get(
    "/permissions",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"]
)
async def request_all_permissions() -> JSONResponse:
    result = await get_all_permissions()
    return result

@permission_router.get(
    "/permissions/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"]
)
async def request_permission(id: UUID = Path(...)) -> JSONResponse:
    result = await get_permission(id)
    return result

@permission_router.put(
    "/permissions/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"]
)
async def put_permission(data: UpdatePermissionSchema,id: UUID = Path(...)) -> JSONResponse:
    result = await update_permission(data,id)
    return result

@permission_router.delete(
    "/permissions/{id}",
    response_description="",
    description="",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["permissions"]
)
async def del_users(id: UUID = Path(...)) -> JSONResponse:
    result = await delete_permission(id)
    return result


