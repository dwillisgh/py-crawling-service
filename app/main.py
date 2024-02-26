import sys

import orjson
import uvicorn
from fastapi import FastAPI, HTTPException, Response
from fastapi.exception_handlers import http_exception_handler
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.api.core.config import settings
from app.api.core.utils import app_startup, app_shutdown
from app.api.routers import v1_api
from app.api.routers.errors import GenericException, internal_error_handler


async def _health_check():
    return Response(status_code=200)


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        # TODO : update links
        description="""
        1. https://github.com/monster-next/jobs-remote-detection-service
        """,
        debug=settings.DEBUG,
        version=settings.VERSION,
        on_startup=[app_startup],
        on_shutdown=[app_shutdown]
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(GenericException, internal_error_handler)
    application.add_exception_handler(Exception, internal_error_handler)

    application.add_api_route("/health", _health_check)
    application.add_api_route("/", lambda: RedirectResponse("/docs"))

    application.include_router(v1_api.router, prefix="/jobs-py-crawling-service")

    application.debug = True

    return application


app = get_application()

orjson_options = orjson.OPT_NAIVE_UTC


def serialize(record: dict) -> str:
    subset = {
        'timestamp': record['time'].isoformat(),
        'level': record['level'].name,
        'message': record['message'],
        'source': f'{record["file"].name}:{record["function"]}:{record["line"]}',
    }
    subset.update(record['extra'])
    return orjson.dumps(subset, default=str, option=orjson_options).decode()


def init_loguru() -> None:
    logger.remove()
    logger.add(lambda message: print(serialize(message.record), file=sys.stdout))


init_loguru()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, use_colors=True, workers=4)
