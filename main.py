from fastapi import FastAPI
from fastapi_pagination import add_pagination

from seeders import run_seeders
from src.controllers import register_routes
from src.exceptions import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

register_routes(app)

run_seeders()

add_pagination(app)
