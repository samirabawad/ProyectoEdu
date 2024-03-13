from fastapi import FastAPI, Request, Depends, BackgroundTasks
from routers import users, empleados, refrigeradores, registros_temp
from internal import admin
from typing import Annotated

from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse
import time
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from schema import userSchema
from model import usersModel
import crud
from database import SessionLocal, engine
from dependencies import get_query_token, get_token_header

#crea las tablas de la bd
usersModel.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "admin",
        "description": "Manejo del rol de administrador. La **configuración** de la app.",
    },
    {
        "name": "empleados",
        "description": "Manejo de empleados.",
    },
    {
        "name": "refrigeradores",
        "description": "Manejo de los refrigeradores.",
    },
    {
        "name": "registros_temperaturas",
        "description": "Manejo de los registros de temperaturas.",
    },
]

#instancia de fastapi
app = FastAPI(openapi_tags=tags_metadata) #global dependencies

#se incluye a la instancia de la app, las rutas del router.
app.include_router(users.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
app.include_router(empleados.router)
app.include_router(refrigeradores.router)
app.include_router(registros_temp.router)



@app.get("/")
async def read_main():
    return {"msg": "Hola Mundo desde el main :D"}

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


#envia un mensaje a log.txt, que podria ser un email.
def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}