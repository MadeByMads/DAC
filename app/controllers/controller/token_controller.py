# from app.controllers.schemas.schemas import JwtPayload
from app.services.jwt_service import JWTOperations
from fastapi import APIRouter, Body
from starlette.responses import JSONResponse

jwt_router = APIRouter(prefix="/token")


@jwt_router.post(
    "",
    response_description="",
    description="",
    tags=["token"],
)
async def generate_token(data: str = Body(..., embed=True)) -> JSONResponse:
    result = await JWTOperations().jwt_encode(data)
    return result
