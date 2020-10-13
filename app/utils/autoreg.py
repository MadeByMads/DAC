from app.utils.acl import get_endpoint_by_name
from app.utils.acl import create_service
from app.controllers.controller.schemas import ServiceSchema
import asyncio


async def autoreg(app):
    """[Auto registration endpoints in DAC]

    Args:
        app: [Instance of Fastapi app]
    """

    # endpoints in exclude_list is not registered in DAC
    exclude_list = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc", "/metrics/"]

    await asyncio.sleep(1)

    registration_list = []
    for route in app.routes:
        if route.path not in exclude_list:
            try:
                endpoint_method = route.methods.pop()
                service = route.tags
                path = route.path
                registration_list.append(
                    {
                        "endpoint_method": endpoint_method,
                        "service": service[0],
                        "path": path
                    }
                )
            except Exception as err:
                print(err)
    # [print(i) for i in registration_list]

    data = ServiceSchema(name="hasan")
    result = await create_service(data)


