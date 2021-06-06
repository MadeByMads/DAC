from app.controllers.schemas.schemas import PermissionCheckSchema
from app.services.permission_service import PermissionService
from core.factories import settings
from fastapi import APIRouter
from starlette.responses import JSONResponse

check_permission_router = APIRouter()


@check_permission_router.post(
    "/check/permission",
    response_description="",
    description="Check Permission",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["check permission"],
)
async def check_permission(data: PermissionCheckSchema) -> JSONResponse:

    return await PermissionService().check_permission(data)
