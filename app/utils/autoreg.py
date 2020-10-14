from app.utils.acl import get_endpoint_by_name
from app.controllers.controller.schemas import ServiceSchema
from core.factories import settings
from starlette.responses import JSONResponse
from core.extensions import log
import asyncio
from http import HTTPStatus
import httpx


async def autoreg(app):
    """[Auto registration endpoints in DAC]
    Args:
        app: [Instance of Fastapi app]
    """

    # endpoints in exclude_list is not registered in DAC
    exclude_list = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc", "/metrics/"]
    service_name = settings.SERVICE_NAME 

    await asyncio.sleep(1)

    prefixes = set()
    for route in app.routes:
        if route.path not in exclude_list:
            try:
                endpoint_method = route.methods.pop()
                path = route.path
                prefixes.add(path)
            except Exception as err:
                log.error(err, exc_info=True)
    service_id = await create_service(service_name)
    await create_endpoints(service_id, prefixes)


async def create_endpoints(service_id: str, prefixes: set):
    for prefix in prefixes:
        async with httpx.AsyncClient() as client:
            await client.post(f"{settings.PERMISSION_SERVICE}/endpoints", 
                                                json={"service_id": service_id, "prefix": prefix}
                                                )


async def create_service(service_name):
    # In one async client we can not send 2 requests. 

    # Get service_name from database. Return id if exists
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.PERMISSION_SERVICE}/services/by-name/{service_name}")
        if response.status_code == HTTPStatus.OK:
            log.info(f"{response.json().get('name')} exists")
            return response.json().get("id")
    
    # Create service_name if not exists
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.PERMISSION_SERVICE}/services", json = {"name": service_name})
        log.info(f"{response.json().get('name')} created")
        return response.json().get("id")
    


    

    


    


