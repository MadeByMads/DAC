from fastapi import (
    APIRouter,
)
from app.controllers.schemas.schemas import (
   PermissionCheckSchema
)
from app.utils.acl import (
   has_permission
)
from typing import List
from starlette.responses import JSONResponse
from core.factories import settings



check_permission_router = APIRouter()


@check_permission_router.post(
    "/check/permission",
    response_description="",
    description="Check Permission",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["check permission"]
)
async def check_permission(data: PermissionCheckSchema) -> JSONResponse:
 
   return await  has_permission(data)
   
   
   