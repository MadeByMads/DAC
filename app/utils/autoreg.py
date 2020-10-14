from app.utils.acl import get_endpoint_by_name
from app.utils.acl import create_service, get_service_by_name
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
        # if route.path not in exclude_list:
        #     for i in dir(route):
        #         print(i, " -> ", getattr(route, i))
        #     break
        if route.path not in exclude_list:
            try:
                endpoint_method = route.methods.pop()
                path = route.path
                prefixes.add(path)
                # registration_list.append(
                #     {
                #         # "method": endpoint_method,
                #         "prefix": path
                #     }
                # )
            except Exception as err:
                print(err)
    # [print(i) for i in registration_list]
    print(prefixes)


    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.PERMISSION_SERVICE}/services/by-name/{service_name}")
        if response.status_code == HTTPStatus.OK:
            service_id = response.json().get("id")
        else:
            pass
            # create service
    

    


    

    


    


