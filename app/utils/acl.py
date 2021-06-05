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
    PermissionCheckSchema,
    PermissionSchema,
    PermissionSchemaDB,
    ServiceSchema,
    ServiceSchemaDB,
    UpdateEndpointSchema,
    UpdatePermissionSchema,
    UpdateUserGroupSchema,
    UpdateUserSchema,
    UserGroupSchema,
    UserGroupSchemaDB,
    UserSchema,
    UserSchemaDB,
)
from app.data.models import (
    Endpoint,
    Groups,
    Method,
    Permission,
    Service,
    User_Groups,
    Users,
)
from core.extensions import db, log
from fastapi import HTTPException
from pydantic import parse_obj_as
from sqlalchemy import and_
from starlette.responses import JSONResponse

# --------------- CREATE -----------------------

NOT_FOUND_MSG = "Not Found"


def clean_dict(data: dict) -> dict:
    return {key: val for (key, val) in data.items() if val is not None}


async def create_user(data: UserSchema) -> Union[UserCreation, JSONResponse]:
    try:
        async with db.transaction():
            user = await Users.create(**data.dict())

            return UserCreation.from_orm(user)

    except Exception as err:
        log.error(f"Error on create_user function ->  {err}")
        return JSONResponse(
            content={"result": False}, status_code=HTTPStatus.BAD_REQUEST
        )


async def create_group(data: GroupSchema):
    try:
        async with db.transaction():
            group = await Groups.create(**data.dict())
            return GroupSchemaDB.from_orm(group)
    except Exception as err:
        log.error(f"Error on create_group function ->  {err}")
        return JSONResponse(
            content={"result": False}, status_code=HTTPStatus.BAD_REQUEST
        )


async def create_us_gr(data: UserGroupSchema):
    try:
        async with db.transaction():
            user_gr = await User_Groups.create(**data.dict())
            return UserGroupSchemaDB.from_orm(user_gr)
    except Exception as err:
        log.error(f"Error on create_us_gr function ->  {err}")
        return JSONResponse(
            content={"result": False}, status_code=HTTPStatus.BAD_REQUEST
        )


async def create_service(data: ServiceSchema):
    try:
        async with db.transaction():
            response = await Service.create(**data.dict())
            return ServiceSchemaDB.from_orm(response)
    except Exception as err:
        log.error(f"Error on create_service function ->  {err}")
        return JSONResponse(
            content={"result": False}, status_code=HTTPStatus.BAD_REQUEST
        )


async def create_endpoint(data: EndpointSchema):
    try:
        async with db.transaction():
            endpoint = await Endpoint.create(**data.dict())
            return EndpointSchemaDB.from_orm(endpoint)
    except Exception as err:
        log.error(f"Error on create_endpoint function ->  {err}")
        return JSONResponse(
            content={"result": False}, status_code=HTTPStatus.BAD_REQUEST
        )


async def create_method(data: MethodSchema):
    try:
        async with db.transaction():
            methods = await Method.create(**data.dict())
            return MethodSchemaDB.from_orm(methods)
    except Exception as err:
        log.error(f"Error on create_method function ->  {err}")
        return JSONResponse(
            content={"result": False}, status_code=HTTPStatus.BAD_REQUEST
        )


async def create_permission(data: PermissionSchema):
    try:
        async with db.transaction():
            permission = await Permission.create(**data.dict())
            return PermissionSchemaDB.from_orm(permission)
    except Exception as err:
        log.error(f"Error on create_permission function ->  {err}")
        return JSONResponse(
            content={"result": False}, status_code=HTTPStatus.BAD_REQUEST
        )


# --------------- UPDATE -----------------------


async def update_user(data: UpdateUserSchema, id: UUID):
    async with db.transaction():
        user = await Users.query.where(Users.id == id).gino.first()
        if user:
            data = clean_dict(data.dict())
            await user.update(**data).apply()
            return UpdateUserSchema.from_orm(user)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def update_group(data: GroupSchema, id: UUID):
    async with db.transaction():
        group = await Groups.query.where(Groups.id == id).gino.first()
        if group:
            data = clean_dict(data.dict())
            await group.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def update_us_gr(data: UpdateUserGroupSchema, id: UUID):
    async with db.transaction():
        group = await User_Groups.query.where(User_Groups.id == id).gino.first()
        if group:
            data = clean_dict(data.dict())
            await group.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def update_service(data: ServiceSchema, id: UUID):
    async with db.transaction():
        service = await Service.query.where(Service.id == id).gino.first()
        if service:
            data = clean_dict(data.dict())
            await service.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def update_endpoint(data: Endpoint, id: UUID):
    async with db.transaction():
        endpoint = await Endpoint.query.where(Endpoint.id == id).gino.first()
        if endpoint:
            data = clean_dict(data.dict())
            await endpoint.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def update_method(data: MethodSchema, id: UUID):
    async with db.transaction():
        method = await Method.query.where(Method.id == id).gino.first()
        if method:
            data = clean_dict(data.dict())
            await method.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def update_permission(data: UpdatePermissionSchema, id: UUID):
    async with db.transaction():
        permission = await Permission.query.where(Permission.id == id).gino.first()
        if permission:
            data = clean_dict(data.dict())
            await permission.update(**data).apply()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


# --------------- DELETE -----------------------


async def delete_user(id: UUID):
    async with db.transaction():
        user = await Users.query.where(Users.id == id).gino.first()
        if user:
            await user.delete()

            return ResponseSchema(result=True).dict()
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def delete_group(id: UUID):
    async with db.transaction():
        group = await Groups.query.where(Groups.id == id).gino.first()
        if group:
            await group.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def delete_us_gr(id: UUID):
    async with db.transaction():
        group = await User_Groups.query.where(User_Groups.id == id).gino.first()
        if group:
            await group.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def delete_service(id: UUID):
    async with db.transaction():
        service = await Service.query.where(Service.id == id).gino.first()
        if service:
            await service.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def delete_endpoint(id: UUID):
    async with db.transaction():
        endpoint = await Endpoint.query.where(Endpoint.id == id).gino.first()
        if endpoint:
            await endpoint.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def delete_method(id: UUID):
    async with db.transaction():
        method = await Method.query.where(Method.id == id).gino.first()
        if method:
            await method.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def delete_permission(id: UUID):
    async with db.transaction():
        permission = await Permission.query.where(Permission.id == id).gino.first()
        if permission:
            await permission.delete()
            return JSONResponse(content={"result": True}, status_code=HTTPStatus.OK)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


# --------------- GET -----------------------


async def get_user(id: UUID):
    async with db.transaction():
        user = await Users.query.where(Users.id == id).gino.first()
        if user:
            return UserSchemaDB.from_orm(user)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_group(id: UUID):
    async with db.transaction():
        group = await Groups.query.where(Groups.id == id).gino.first()
        if group:
            return GroupSchemaDB.from_orm(group)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_us_gr(id: UUID):
    async with db.transaction():
        group = await User_Groups.query.where(User_Groups.id == id).gino.first()
        if group:
            return UserGroupSchemaDB.from_orm(group)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_service(id: UUID):
    async with db.transaction():
        service = await Service.query.where(Service.id == id).gino.first()
        if service:
            return ServiceSchemaDB.from_orm(service)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_endpoint(id: UUID):
    async with db.transaction():
        endpoint = await Endpoint.query.where(Endpoint.id == id).gino.first()
        if endpoint:
            return EndpointSchemaDB.from_orm(endpoint)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_method(id: UUID):
    async with db.transaction():
        method = await Method.query.where(Method.id == id).gino.first()
        if method:
            return MethodSchemaDB.from_orm(method)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_permission(id: UUID):
    async with db.transaction():
        permission = await Permission.query.where(Permission.id == id).gino.first()
        if permission:
            return PermissionSchemaDB.from_orm(permission)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


# --------------- GET BY NAME-----------------------


async def get_method_by_name(name: str):
    async with db.transaction():
        method = await Method.query.where(Method.name == name).gino.first()
        if method:
            return MethodSchemaDB.from_orm(method)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_endpoint_by_name(name: str):
    async with db.transaction():
        endpoint = await Endpoint.query.where(Endpoint.name == name).gino.first()
        if endpoint:
            return EndpointSchemaDB.from_orm(endpoint)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_service_by_name(name: str):
    async with db.transaction():
        service = await Service.query.where(Service.name == name).gino.first()
        if service:
            return ServiceSchemaDB.from_orm(service)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_endpoint_by_svc_prefix(id: UUID, prefix: str):
    async with db.transaction():
        endpoint = await Endpoint.query.where(
            and_(Endpoint.service_id == id, Endpoint.prefix == prefix)
        ).gino.first()
        if endpoint:
            return EndpointSchemaDB.from_orm(endpoint)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


# --------------- GET ALL-----------------------


async def get_all_user():
    async with db.transaction():
        users = await Users.query.gino.all()
        if users:
            return parse_obj_as(List[UserSchemaDB], users)

        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_all_group():
    async with db.transaction():
        groups = await Groups.query.gino.all()
        if groups:
            return parse_obj_as(List[GroupSchemaDB], groups)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_all_us_gr():
    async with db.transaction():
        groups = await User_Groups.query.gino.all()
        if groups:
            return parse_obj_as(List[UserGroupSchemaDB], groups)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_all_service():
    async with db.transaction():
        services = await Service.query.gino.all()
        if services:
            return parse_obj_as(List[ServiceSchemaDB], services)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_all_method():
    async with db.transaction():
        methods = await Method.query.gino.all()
        if methods:
            return parse_obj_as(List[MethodSchemaDB], methods)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_all_permissions():
    async with db.transaction():
        permissions = await Permission.query.gino.all()
        if permissions:
            return parse_obj_as(List[PermissionSchemaDB], permissions)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


async def get_all_endpoints():
    async with db.transaction():
        endpoints = await Endpoint.query.gino.all()
        if endpoints:
            return parse_obj_as(List[EndpointSchemaDB], endpoints)
        raise HTTPException(detail=NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)


# --------------- Check Permissions --------------------------


async def has_permission(data: PermissionCheckSchema) -> bool:
    service = await get_service_by_name(data.service)
    endpoint = await get_endpoint_by_svc_prefix(service.id, data.endpoint)
    method = await get_method_by_name(data.method)
    log.warning(f"service id - > {service}")
    log.warning(f"endpoint id - > {endpoint}")
    log.warning(f"method id - > {method}")

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
        return JSONResponse(content={"result": False}, status_code=HTTPStatus.FORBIDDEN)

    permission = await check_permission(
        data.entity, data.entity_type, service.id, method.id, endpoint.id
    )

    return JSONResponse(
        content={"result": bool(permission)},
        status_code=HTTPStatus.OK if permission else HTTPStatus.FORBIDDEN,
    )


async def check_permission(
    entity: str, entity_type: str, service_id: UUID, method_id: UUID, endpoint_id: UUID
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
