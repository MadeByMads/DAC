from core.factories import settings
from datetime import datetime, timedelta
from app.data.models import (
    Users,
    User_Groups,
    Groups,
    Service,
    Endpoint,
    Method,
    Permission,

)
from pydantic import parse_obj_as
from uuid import UUID
from fastapi import HTTPException
from fastapi import Header
from core.extensions import log
from sqlalchemy import and_
from app.controllers.controller.schemas import (
    UserSchema,
    UserSchemaDB,
    UserGroupSchema,
    UserGroupSchemaDB,
    GroupSchema,
    GroupSchemaDB,
    ServiceSchema,
    ServiceSchemaDB,
    EndpointSchema,
    EndpointSchemaDB,
    MethodSchema,
    MethodSchemaDB,
    PermissionSchema, 
    PermissionSchemaDB,
    UpdateEndpointSchema,
    UpdatePermissionSchema,
    UpdateUserGroupSchema,
    UpdateUserSchema,
    PermissionCheckSchema
   
)
from core.extensions import db
from starlette.responses import JSONResponse
from http import HTTPStatus
from typing import List
import jwt, json,hashlib
from app.controllers.schemas.response_schema import UserCreation, ResponseSchema
from typing import Optional, List, Union, Mapping, Any, Dict

# --------------- CREATE -----------------------

def clean_dict(data : dict) -> dict:
    return {key: val for (key, val) in data.items() if val is not None}


async def create_user(data: UserSchema) -> Union[UserCreation, JSONResponse]:
    try:
        async with db.transaction() as ctx:    
            user = await Users.create(**data.dict())

            return UserCreation.from_orm(user)

    except Exception as err:
        log.error(f"Error on create_user function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def create_group(data: GroupSchema):
    try:
        async with db.transaction() as ctx:
            group = await Groups.create(**data.dict())
            return GroupSchemaDB.from_orm(group)
    except Exception as err:
        log.error(f"Error on create_group function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def create_us_gr(data: UserGroupSchema):
    try:
        async with db.transaction() as ctx:
            user_gr = await User_Groups.create(**data.dict())
            return UserGroupSchemaDB.from_orm(user_gr)
    except Exception as err:
        log.error(f"Error on create_us_gr function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def create_service(data: ServiceSchema):
    try:
        async with db.transaction() as ctx:
            response = await Service.create(**data.dict())
            return ServiceSchemaDB.from_orm(response)
    except Exception as err:
        log.error(f"Error on create_service function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def create_endpoint(data: EndpointSchema):
    try:
        async with db.transaction() as ctx:
            endpoint = await Endpoint.create(**data.dict())
            return EndpointSchemaDB.from_orm(endpoint)
    except Exception as err:
        log.error(f"Error on create_endpoint function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def create_method(data: MethodSchema):
    try:
        async with db.transaction() as ctx:
            methods = await Method.create(**data.dict())
            return MethodSchemaDB.from_orm(methods)
    except Exception as err:
        log.error(f"Error on create_method function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def create_permission(data: PermissionSchema):
    try:
        async with db.transaction() as ctx:
            permission = await Permission.create(**data.dict())
            return PermissionSchemaDB.from_orm(permission)
    except Exception as err:
        log.error(f"Error on create_permission function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)



# --------------- UPDATE -----------------------

async def update_user(data: UpdateUserSchema,id: UUID):
    try:
        async with db.transaction() as ctx:
            user = await Users.query.where(Users.id == id).gino.first()
            if user:
                data =  clean_dict(data.dict())
                await user.update(**data).apply()
                return UpdateUserSchema.from_orm(user)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)

    except Exception as err:
        log.error(f"Error on update_user function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def update_group(data: GroupSchema,id: UUID):
    try:
        async with db.transaction() as ctx:
            group = await Groups.query.where(Groups.id == id).gino.first()
            if group:
                data =  clean_dict(data.dict())
                await group.update(**data).apply()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)

    except Exception as err:
        log.error(f"Error on update_group function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def update_us_gr(data: UpdateUserGroupSchema,id: UUID):
    try:
        async with db.transaction() as ctx:
            group = await User_Groups.query.where(User_Groups.id == id).gino.first()
            if group:
                data =  clean_dict(data.dict())
                await group.update(**data).apply()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)

    except Exception as err:
        log.error(f"Error on update_us_gr function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def update_service(data: ServiceSchema,id: UUID):
    try:
        async with db.transaction() as ctx:
            service = await Service.query.where(Service.id == id).gino.first()
            if service:
                data =  clean_dict(data.dict())
                await service.update(**data).apply()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)

    except Exception as err:
        log.error(f"Error on update_us_gr function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)



async def update_endpoint(data: Endpoint,id: UUID):
    try:
        async with db.transaction() as ctx:
            endpoint = await Endpoint.query.where(Endpoint.id == id).gino.first()
            if endpoint:
                data =  clean_dict(data.dict())
                await endpoint.update(**data).apply()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)

    except Exception as err:
        log.error(f"Error on update_endpoint function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def update_method(data: MethodSchema,id: UUID):
    try:
        async with db.transaction() as ctx:
            method = await Method.query.where(Method.id == id).gino.first()
            if method:
                data =  clean_dict(data.dict())
                await method.update(**data).apply()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)

    except Exception as err:
        log.error(f"Error on update_method function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def update_permission(data: UpdatePermissionSchema,id: UUID):
    try:
        async with db.transaction() as ctx:
            permission = await Permission.query.where(Permission.id == id).gino.first()
            if permission:
                data =  clean_dict(data.dict())
                await permission.update(**data).apply()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)

    except Exception as err:
        log.error(f"Error on update_permission function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)



# --------------- DELETE -----------------------



async def delete_user(id: UUID):
    try:
        async with db.transaction() as ctx:
            user = await Users.query.where(Users.id == id).gino.first()
            if user:
                await user.delete()
                
                return ResponseSchema(result=True).dict()
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on delete_user function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def delete_group(id: UUID):
    try:
        async with db.transaction() as ctx:
            group = await Groups.query.where(Groups.id == id).gino.first()
            if group:
                await group.delete()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on delete_group function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def delete_us_gr(id: UUID):
    try:
        async with db.transaction() as ctx:
            group = await User_Groups.query.where(User_Groups.id == id).gino.first()
            if group:
                await group.delete()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on delete_us_gr function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def delete_service(id: UUID):
    try:
        async with db.transaction() as ctx:
            service = await Service.query.where(Service.id == id).gino.first()
            if service:
                await service.delete()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on delete_service function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def delete_endpoint(id: UUID):
    try:
        async with db.transaction() as ctx:
            endpoint = await Endpoint.query.where(Endpoint.id == id).gino.first()
            if endpoint:
                await endpoint.delete()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on delete_endpoint function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)



async def delete_method(id: UUID):
    try:
        async with db.transaction() as ctx:
            method = await Method.query.where(Method.id == id).gino.first()
            if method:
                await method.delete()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on delete_method function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def delete_permission(id: UUID):
    try:
        async with db.transaction() as ctx:
            permission = await Permission.query.where(Permission.id == id).gino.first()
            if permission:
                await permission.delete()
                return JSONResponse(content={"result": True},status_code=HTTPStatus.OK)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on delete_permission function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)




# --------------- GET -----------------------


async def get_user(id: UUID):
    try:
        async with db.transaction() as ctx:
            user = await Users.query.where(Users.id == id).gino.first()
            if user:
                return UserSchemaDB.from_orm(user)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_user function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_group(id: UUID):
    try:
        async with db.transaction() as ctx:
            group = await Groups.query.where(Groups.id == id).gino.first()
            if group:
                return GroupSchemaDB.from_orm(group)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_group function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_us_gr(id: UUID):
    try:
        async with db.transaction() as ctx:
            group = await User_Groups.query.where(User_Groups.id == id).gino.first()
            if group:
                return UserGroupSchemaDB.from_orm(group)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_us_gr function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_service(id: UUID):
    try:
        async with db.transaction() as ctx:
            service = await Service.query.where(Service.id == id).gino.first()
            if service:
                return ServiceSchemaDB.from_orm(service)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_service function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_endpoint(id: UUID):
    try:
        async with db.transaction() as ctx:
            endpoint = await Endpoint.query.where(Endpoint.id == id).gino.first()
            if endpoint:
                return EndpointSchemaDB.from_orm(endpoint)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_endpoint function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_method(id: UUID):
    try:
        async with db.transaction() as ctx:
            method = await Method.query.where(Method.id == id).gino.first()
            if method:
                return MethodSchemaDB.from_orm(method)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_method function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_permission(id: UUID):
    try:
        async with db.transaction() as ctx:
            permission = await Permission.query.where(Permission.id == id).gino.first()
            if permission:
               return PermissionSchemaDB.from_orm(permission)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_permission function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


# --------------- GET BY NAME-----------------------

async def get_method_by_name(name: str):
    try:
        async with db.transaction() as ctx:
            method = await Method.query.where(Method.name == name).gino.first()
            if method:
                return MethodSchemaDB.from_orm(method)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_method_by_name function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)

    
async def get_endpoint_by_name(name: str):
    try:
        async with db.transaction() as ctx:
            endpoint = await Endpoint.query.where(Endpoint.name == name).gino.first()
            if endpoint:
                return EndpointSchemaDB.from_orm(endpoint)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_endpoint_by_name function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_service_by_name(name: str):
    try:
        async with db.transaction() as ctx:
            service = await Service.query.where(Service.name == name).gino.first()
            if service:
                return ServiceSchemaDB.from_orm(service)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_endpoint_by_name function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_endpoint_by_svc_prefix(id: UUID, prefix: str):
    try:
        async with db.transaction() as ctx:
            endpoint = await Endpoint.query.where(and_(Endpoint.service_id == id, Endpoint.prefix == prefix)).gino.first()
            if endpoint:
                return EndpointSchemaDB.from_orm(endpoint)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_endpoint function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)

# --------------- GET ALL-----------------------



async def get_all_user():
    try:
        async with db.transaction() as ctx:
            users = await Users.query.gino.all()
            if users:
                return parse_obj_as(List[UserSchemaDB],users)

            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_all_user function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_all_group():
    try:
        async with db.transaction() as ctx:
            groups = await Groups.query.gino.all()
            if groups:
                return parse_obj_as(List[GroupSchemaDB],groups)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_all_group function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_all_us_gr():
    try:
        async with db.transaction() as ctx:
            groups = await User_Groups.query.gino.all()
            if groups:
                return parse_obj_as(List[UserGroupSchemaDB],groups)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_all_us_gr function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)


async def get_all_service():
    try:
        async with db.transaction() as ctx:
            services = await Service.query.gino.all()
            if services:
                return parse_obj_as(List[ServiceSchemaDB],services)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_all_service function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)



async def get_all_method():
    try:
        async with db.transaction() as ctx:
            methods = await Method.query.gino.all()
            if methods:
                return parse_obj_as(List[MethodSchemaDB],methods)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_all_method function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)




async def get_all_permissions():
    try:
        async with db.transaction() as ctx:
            permissions = await Permission.query.gino.all()
            if permissions:
               return parse_obj_as(List[PermissionSchemaDB],permissions)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_all_permissions function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)



async def get_all_endpoints():
    try:
        async with db.transaction() as ctx:
            endpoints = await Endpoint.query.gino.all()
            if endpoints:
               return parse_obj_as(List[EndpointSchemaDB], endpoints)
            return JSONResponse(content={"result": False},status_code=HTTPStatus.NOT_FOUND)
    except Exception as err:
        log.error(f"Error on get_all_permissions function ->  {err}")
        return JSONResponse(content={"result": False},status_code=HTTPStatus.BAD_REQUEST)



# --------------- Check Permissions --------------------------




async def has_permission(data: PermissionCheckSchema) -> bool:
    service = await get_service_by_name(data.service)
    endpoint = await get_endpoint_by_svc_prefix(service.id, data.endpoint)
    method = await get_method_by_name(data.method)
    log.warning(f"service id - > {service}")
    log.warning(f"endpoint id - > {endpoint}")
    log.warning(f"method id - > {method}")

    if isinstance(service, JSONResponse) or isinstance(endpoint,JSONResponse) or isinstance(method, JSONResponse):
        return JSONResponse(
                content={"result": False}, status_code=HTTPStatus.FORBIDDEN
            )

    if data.entity_type == "USER_GROUPS":
        entity = await User_Groups.query.where(
            User_Groups.group_id == data.entity
        ).gino.first()
        
    elif data.entity_type == "USERS":
        entity = await Users.query.where(Users.identity == data.entity).gino.first()
        user_groups = await User_Groups.query.where(User_Groups.user_id == data.entity).gino.all()
        print("user_groups -> ", user_groups)
    
    elif data.entity_type == "SERVICE":
        entity = await Service.query.where(Service.id == data.entity).gino.first()
    
         

    print("ENTITIY " ,entity.id)
    if not entity:
        return JSONResponse(
            content={"result": False}, status_code=HTTPStatus.FORBIDDEN
        )

    permission = await check_permission(
        entity,
        data.entity_type,
        method.id,
        endpoint.id
    )

    return JSONResponse(
                content={"result": True if permission else False}, status_code=HTTPStatus.OK if permission else HTTPStatus.FORBIDDEN
            )


async def check_permission(
    entity: str,
    entity_type: str,
    method_id: UUID,
    endpoint_id: UUID
):
    return await Permission.query.where(
        and_(
            Permission.endpoint_id == endpoint_id,
            Permission.method_id == method_id,
            Permission.entity == str(entity),
            Permission.entity_type == entity_type
        )
    ).gino.first()