from fastapi import APIRouter, HTTPException,Cookie, Depends,Header,File, Body,Query
from starlette.responses import JSONResponse
from core.factories import settings
from app.controllers.controller.schemas import *
import  httpx

router = APIRouter()


@router.get("/",tags=["Test"],
response_description="test",
description="test",
include_in_schema=settings.INCLUDE_SCHEMA,)
async def test_test(test: dict=Body(...,example={"mytest": "mytest" })) -> JSONResponse:


    return JSONResponse({"result" : True})

@router.get("/test",tags=["Test"],
response_description="test",
description="test",
include_in_schema=settings.INCLUDE_SCHEMA,)
async  def test_2(test: str= Query(None, alias="token", title="token", description="Send token in the query"))-> JSONResponse:

    return JSONResponse({"result" : True})

