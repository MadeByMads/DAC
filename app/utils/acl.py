import logging
from http import HTTPStatus
from typing import List, Union
from uuid import UUID

from app.controllers.schemas.response_schema import ResponseSchema, UserCreation
from app.controllers.schemas.schemas import (
    EndpointSchema,
    EndpointSchemaDB,
    GroupSchema,
    GroupSchemaDB,
    MethodSchema,
    MethodSchemaDB,
    PermissionSchema,
    PermissionSchemaDB,
    ServiceSchema,
    ServiceSchemaDB,
    UpdatePermissionSchema,
    UpdateUserGroupSchema,
    UpdateUserSchema,
    UserGroupSchema,
    UserGroupSchemaDB,
    UserSchema,
    UserSchemaDB,
)
from app.data.models import (
    USER_TYPES,
    Endpoint,
    Groups,
    Method,
    Permission,
    Service,
    User_Groups,
    Users,
)
from app.utils.log_helper import log_function
from core.extensions import db
from fastapi import HTTPException
from pydantic import parse_obj_as
from sqlalchemy import and_
from starlette.responses import JSONResponse

# --------------- CREATE -----------------------

NOT_FOUND_MSG = "Not Found"

logger = logging.getLogger(__name__)
log = log_function(logger)


def clean_dict(data: dict) -> dict:
    return {key: val for (key, val) in data.items() if val is not None}


@log
async def create_user(data: UserSchema) -> Union[UserCreation, JSONResponse]:
    async with db.transaction():
        user = await Users.query.where(Users.identity == data.identity).gino.first()
        if user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        user = await Users.create(**data.dict())
        return UserCreation.from_orm(user)


@log
async def create_group(data: GroupSchema):
    async with db.transaction():
        group = await Groups.query.where(Groups.name == data.name).gino.first()
        if group:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        group = await Groups.create(name=USER_TYPES(data.name))
        return GroupSchemaDB.from_orm(group)


@log
async def create_us_gr(data: UserGroupSchema):
    async with db.transaction():
        user_gr = await User_Groups.query.where(
            and_(
                User_Groups.group_id == data.group_id,
                User_Groups.user_id == data.user_id,
            )
        ).gino.first()

        if user_gr:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        user_gr = await User_Groups.create(**data.dict())
        return UserGroupSchemaDB.from_orm(user_gr)


@log
async def create_service(data: ServiceSchema):
    async with db.transaction():
        service = await Service.query.where(Service.name == data.name).gino.first()
        if service:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

        response = await Service.create(**data.dict())
        return ServiceSchemaDB.from_orm(response)


@log
async def create_endpoint(data: EndpointSchema):
    async with db.transaction():
        endpoint = await Endpoint.query.where(
            and_(
                Endpoint.service_id == data.service_id,
                Endpoint.prefix == data.prefix,
            )
        ).gino.first()
        if endpoint:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

        endpoint = await Endpoint.create(**data.dict())
        return EndpointSchemaDB.from_orm(endpoint)


@log
async def create_method(data: MethodSchema):
    async with db.transaction():
        methods = await Method.query.where(Method.name == data.name).gino.first()
        if methods:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

        methods = await Method.create(**data.dict())
        return MethodSchemaDB.from_orm(methods)


@log
async def create_permission(data: PermissionSchema):
    async with db.transaction():
        permission = await Permission.query.where(
            and_(
                Permission.endpoint_id == data.endpoint_id,
                Permission.entity_type == data.entity_type,
                Permission.service_id == data.service_id,
                Permission.method_id == data.method_id,
            )
        ).gino.first()

        if permission:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        permission = await Permission.create(**data.dict())
        return PermissionSchemaDB.from_orm(permission)


# --------------- UPDATE -----------------------


@log
async def update_user(data: UpdateUserSchema, id: UUID):
    async with db.transaction():
        user = await Users.query.where(Users.id == id).gino.first()
        if user:
            data = clean_dict(data.dict())
            await user.update(**data).apply()
            return UpdateUserSchema.from_orm(user)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def update_group(data: GroupSchema, id: UUID):
    async with db.transaction():
        group = await Groups.query.where(Groups.id == id).gino.first()
        if group:
            data = clean_dict(data.dict())
            await group.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def update_us_gr(data: UpdateUserGroupSchema, id: UUID):
    async with db.transaction():
        group = await User_Groups.query.where(User_Groups.id == id).gino.first()
        if group:
            data = clean_dict(data.dict())
            await group.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def update_service(data: ServiceSchema, id: UUID):
    async with db.transaction():
        service = await Service.query.where(Service.id == id).gino.first()
        if service:
            data = clean_dict(data.dict())
            await service.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def update_endpoint(data: Endpoint, id: UUID):
    async with db.transaction():
        endpoint = await Endpoint.query.where(Endpoint.id == id).gino.first()
        if endpoint:
            data = clean_dict(data.dict())
            await endpoint.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def update_method(data: MethodSchema, id: UUID):
    async with db.transaction():
        method = await Method.query.where(Method.id == id).gino.first()
        if method:
            data = clean_dict(data.dict())
            await method.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def update_permission(data: UpdatePermissionSchema, id: UUID):
    async with db.transaction():
        permission = await Permission.query.where(Permission.id == id).gino.first()
        if permission:
            data = clean_dict(data.dict())
            await permission.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


# --------------- DELETE -----------------------


@log
async def delete_user(id: UUID):
    async with db.transaction():
        user = await Users.query.where(Users.id == id).gino.first()
        if user:
            await user.delete()

            return ResponseSchema(result=True).dict()
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def delete_group(id: UUID):
    async with db.transaction():
        group = await Groups.query.where(Groups.id == id).gino.first()
        if group:
            await group.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def delete_us_gr(id: UUID):
    async with db.transaction():
        group = await User_Groups.query.where(User_Groups.id == id).gino.first()
        if group:
            await group.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def delete_service(id: UUID):
    async with db.transaction():
        service = await Service.query.where(Service.id == id).gino.first()
        if service:
            await service.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def delete_endpoint(id: UUID):
    async with db.transaction():
        endpoint = await Endpoint.query.where(Endpoint.id == id).gino.first()
        if endpoint:
            await endpoint.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def delete_method(id: UUID):
    async with db.transaction():
        method = await Method.query.where(Method.id == id).gino.first()
        if method:
            await method.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def delete_permission(id: UUID):
    async with db.transaction():
        permission = await Permission.query.where(Permission.id == id).gino.first()
        if permission:
            await permission.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


# --------------- GET -----------------------


@log
async def get_user(id: UUID):
    async with db.transaction():
        user = await Users.query.where(Users.id == id).gino.first()
        if user:
            return UserSchemaDB.from_orm(user)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def get_group(id: UUID):
    async with db.transaction():
        group = await Groups.query.where(Groups.id == id).gino.first()
        if group:
            return GroupSchemaDB.from_orm(group)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def get_us_gr(id: UUID):
    async with db.transaction():
        group = await User_Groups.query.where(User_Groups.id == id).gino.first()
        if group:
            return UserGroupSchemaDB.from_orm(group)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def get_service(id: UUID):
    async with db.transaction():
        service = await Service.query.where(Service.id == id).gino.first()
        if service:
            return ServiceSchemaDB.from_orm(service)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def get_endpoint(id: UUID):
    async with db.transaction():
        endpoint = await Endpoint.query.where(Endpoint.id == id).gino.first()
        if endpoint:
            return EndpointSchemaDB.from_orm(endpoint)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def get_method(id: UUID):
    async with db.transaction():
        method = await Method.query.where(Method.id == id).gino.first()
        if method:
            return MethodSchemaDB.from_orm(method)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def get_permission(id: UUID):
    async with db.transaction():
        permission = await Permission.query.where(Permission.id == id).gino.first()
        if permission:
            return PermissionSchemaDB.from_orm(permission)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


# --------------- GET BY NAME-----------------------


@log
async def get_method_by_name(name: str):
    async with db.transaction():
        method = await Method.query.where(Method.name == name).gino.first()
        if method:
            return MethodSchemaDB.from_orm(method)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def get_endpoint_by_name(name: str):
    async with db.transaction():
        endpoint = await Endpoint.query.where(Endpoint.name == name).gino.first()
        if endpoint:
            return EndpointSchemaDB.from_orm(endpoint)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def get_service_by_name(name: str):
    async with db.transaction():
        service = await Service.query.where(Service.name == name).gino.first()
        if service:
            return ServiceSchemaDB.from_orm(service)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


@log
async def get_endpoint_by_svc_prefix(id: UUID, prefix: str):
    async with db.transaction():
        endpoint = await Endpoint.query.where(
            and_(Endpoint.service_id == id, Endpoint.prefix == prefix)
        ).gino.first()
        if endpoint:
            return EndpointSchemaDB.from_orm(endpoint)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


# --------------- GET ALL-----------------------


@log
async def get_all_user():
    async with db.transaction():
        users = await Users.query.gino.all()
        return parse_obj_as(List[UserSchemaDB], users)


@log
async def get_all_group():
    async with db.transaction():
        groups = await Groups.query.gino.all()
        return parse_obj_as(List[GroupSchemaDB], groups)


@log
async def get_all_us_gr():
    async with db.transaction():
        groups = await User_Groups.query.gino.all()

        return parse_obj_as(List[UserGroupSchemaDB], groups)


@log
async def get_all_service():
    async with db.transaction():
        services = await Service.query.gino.all()
        return parse_obj_as(List[ServiceSchemaDB], services)


@log
async def get_all_method():
    async with db.transaction():
        methods = await Method.query.gino.all()
        return parse_obj_as(List[MethodSchemaDB], methods)


@log
async def get_all_permissions():
    async with db.transaction():
        permissions = await Permission.query.gino.all()
        return parse_obj_as(List[PermissionSchemaDB], permissions)


@log
async def get_all_endpoints():
    async with db.transaction():
        endpoints = await Endpoint.query.gino.all()
        return parse_obj_as(List[EndpointSchemaDB], endpoints)
