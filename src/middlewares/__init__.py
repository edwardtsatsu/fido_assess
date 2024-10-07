from fastapi import Request

from configs.logger import logger


async def log_middleware(request: Request, call_next):
    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "headers": dict(request.headers),
    }

    logger.info(log_dict, extra=log_dict)

    response = await call_next(request)

    return response
