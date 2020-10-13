def autoreg(app):
    """[Auto registration endpoints in DAC]

    Args:
        app: [Instance of Fastapi app]
    """

    # endpoints in exclude_list is not registered in DAC
    exclude_list = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc", "/metrics/"]

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

    [print(i) for i in registration_list]
