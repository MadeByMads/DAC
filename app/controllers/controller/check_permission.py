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
   PermissionCheckSchema
)
from app.utils.acl import (
   get_method_by_name,
   get_endpoint_by_name
)
from typing import List
from starlette.responses import JSONResponse
from starlette.requests import Request
from core.factories import settings
from typing import Union


check_permission_router = APIRouter()


@check_permission_router.get(
    "/check_permission",
    response_description="",
    description="Check Permission",
    include_in_schema=settings.INCLUDE_SCHEMA,
    tags=["check_permission"]
)
async def check_permission(data: PermissionCheckSchema) -> JSONResponse:

   print("data ---> ", data)
   print("#########################################")

   method = data.method
   endpoint = data.endpoint
   entity = data.entity
   entity_type = data.entity_type
   service = data.service
   

   print("entity ---> ", entity)
   print("entity_type ---> ", entity_type)
   print("method ---> ", method)
   print("service ---> ", service)
   print("endpoint ---> ", endpoint)
   