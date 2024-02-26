import json
from starlette.requests import Request
from starlette.responses import JSONResponse
from loguru import logger


class GenericException(Exception):
    def __init__(
            self,
            http_status_code: int,
            msg: str = None,
    ):
        if not msg:
            msg = f"Generic exception encountered: contact API admin for more details."
        self.content = json.dumps(
            {
                "msg": msg
            }
        )
        self.http_status_code = http_status_code


async def internal_error_handler(
        request: Request, exc: GenericException
) -> JSONResponse:
    if not isinstance(exc, GenericException):
        exc = GenericException(msg=str(exc), http_status_code=500)
    logger.error(exc.content)
    return JSONResponse({"errors": [exc.content]}, status_code=exc.http_status_code)
