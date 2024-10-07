from src.exceptions.user_not_found_exception import UserNotFoundException
from src.exceptions.exception_handler import resource_not_found_exception_handler, user_not_found_exception_handler
from src.exceptions.resource_not_found_exception import ResourceNotFoundException


def register_exception_handlers(app):
    app.add_exception_handler(
        ResourceNotFoundException, resource_not_found_exception_handler
    )
    app.add_exception_handler(
        UserNotFoundException, user_not_found_exception_handler
    )
