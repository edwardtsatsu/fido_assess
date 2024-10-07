from fastapi import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.exceptions.decryption_failed_excpetion import DecryptionFailedException
from src.exceptions.encryption_failed_exception import EncryptionFailedException
from src.exceptions.resource_not_created_exception import ResourceNotCreatedException
from src.exceptions.resource_not_found_exception import ResourceNotFoundException
from src.exceptions.user_not_found_exception import UserNotFoundException


def resource_not_found_exception_handler(
    request: Request, exception: ResourceNotFoundException
):
    return JSONResponse(
        content={"message": exception.description},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def resource_not_created_exception_handler(
    request: Request, exception: ResourceNotCreatedException
):
    return JSONResponse(
        content={"message": exception.description},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def decryption_failed_exception_handler(
    request: Request, exception: DecryptionFailedException
):
    return JSONResponse(
        content={"message": exception.description},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def encryption_failed_exception_handler(
    request: Request, exception: EncryptionFailedException
):
    return JSONResponse(
        content={"message": exception.description},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def user_not_found_exception_handler(
    request: Request, exception: UserNotFoundException
):
    return JSONResponse(
        content={"message": exception.description},
        status_code=status.HTTP_400_BAD_REQUEST,
    )
