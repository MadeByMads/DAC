import logging

from core.extensions import db
from core.factories import settings
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.controllers.controller.acl_cont import acl_router
from app.controllers.controller.check_permission import check_permission_router
from app.controllers.controller.endpoints import endpoint_router
from app.controllers.controller.groups_cont import group_router
from app.controllers.controller.methods_cont import method_router
from app.controllers.controller.permission_cont import permission_router
from app.controllers.controller.service_cont import service_router
from app.controllers.controller.user_group_cont import us_gr_router
from app.utils.migration_setup import MigrationSetup

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

app = FastAPI()
db.init_app(app)


@app.on_event("startup")
async def startup():
    MigrationSetup(settings).process_migration()
    print("app started")


@app.on_event("shutdown")
async def shutdown():
    print("SHUTDOWN")


cors_origins = [i.strip() for i in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
def http_handle(request: Request, ex: HTTPException):
    return JSONResponse(
        status_code=ex.status_code,
        content={"message": ex.detail},
    )


app.include_router(acl_router)
app.include_router(service_router)
app.include_router(group_router)
app.include_router(us_gr_router)
app.include_router(method_router)

app.include_router(permission_router)
app.include_router(check_permission_router)
app.include_router(endpoint_router)
