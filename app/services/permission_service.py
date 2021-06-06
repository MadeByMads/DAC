import logging
from http import HTTPStatus
from uuid import UUID

from app.controllers.schemas.schemas import PermissionCheckSchema
from app.data.models import Permission, Service, User_Groups, Users
from app.utils.acl import (
    get_endpoint_by_svc_prefix,
    get_method_by_name,
    get_service_by_name,
)
from app.utils.log_helper import ClassLogger
from fastapi.responses import JSONResponse
from sqlalchemy import and_

logger = logging.getLogger(__name__)


# --------------- Check Permissions --------------------------


@ClassLogger(logger=logger)
class PermissionService:
    async def has_permission(self, data: PermissionCheckSchema) -> bool:
        service = await get_service_by_name(data.service)
        endpoint = await get_endpoint_by_svc_prefix(service.id, data.endpoint)
        method = await get_method_by_name(data.method)
        logger.warning(f"service id - > {service}")
        logger.warning(f"endpoint id - > {endpoint}")
        logger.warning(f"method id - > {method}")

        if data.entity_type == "USER_GROUPS":
            entity = await User_Groups.query.where(
                User_Groups.group_id == data.entity
            ).gino.first()

        elif data.entity_type == "USERS":
            entity = await Users.query.where(Users.identity == data.entity).gino.first()
            user_groups = await User_Groups.query.where(
                User_Groups.user_id == data.entity
            ).gino.all()
            print("user_groups -> ", user_groups)

        elif data.entity_type == "SERVICE":
            entity = await Service.query.where(Service.name == data.entity).gino.first()

        if not entity:
            return JSONResponse(
                content={"result": False}, status_code=HTTPStatus.FORBIDDEN
            )

        permission = await self.check_permission(
            data.entity, data.entity_type, service.id, method.id, endpoint.id
        )

        return JSONResponse(
            content={"result": bool(permission)},
            status_code=HTTPStatus.OK if permission else HTTPStatus.FORBIDDEN,
        )

    async def check_permission(
        self,
        entity: str,
        entity_type: str,
        service_id: UUID,
        method_id: UUID,
        endpoint_id: UUID,
    ):
        return await Permission.query.where(
            and_(
                Permission.endpoint_id == endpoint_id,
                Permission.method_id == method_id,
                Permission.service_id == service_id,
                Permission.entity == str(entity),
                Permission.entity_type == entity_type,
            )
        ).gino.first()
