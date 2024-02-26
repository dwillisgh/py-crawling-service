from loguru import logger


async def app_startup():
    logger.info("app_startup executed")


async def app_shutdown():
    logger.info("app_shutdown executed")