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
   PermissionSchema,
   PermissionSchemaDB,
   UpdatePermissionSchema
)
from app.utils.acl import (
   get_all_permissions,
   get_permission,
)
from typing import List
from starlette.responses import JSONResponse
from starlette.requests import Request
from core.factories import settings
from typing import Union


check_permission_router = APIRouter()


# @check_permission_router.post(
#     "/check_permission",
#     response_description="",
#     description="Check Permission",
#     include_in_schema=settings.INCLUDE_SCHEMA,
#     tags=["check_permission"]
# )
# async def check_permission(data: PermissionSchema) -> JSONResponse: