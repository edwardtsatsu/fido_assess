from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.base import BaseHTTPMiddleware

from seeders import run_seeders
from src.controllers import register_routes
from src.exceptions import register_exception_handlers
from src.middlewares import log_middleware

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

register_exception_handlers(app)

register_routes(app)


run_seeders()

add_pagination(app)
