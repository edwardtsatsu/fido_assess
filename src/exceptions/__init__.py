from src.exceptions.exception_handler import \
    resource_not_found_exception_handler
from src.exceptions.resource_not_found_exception import \
    ResourceNotFoundException


def register_exception_handlers(app):
    app.add_exception_handler(
        ResourceNotFoundException, resource_not_found_exception_handler
    )
