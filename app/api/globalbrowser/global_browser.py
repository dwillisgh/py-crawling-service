from playwright.async_api import async_playwright
from loguru import logger


class GlobalBrowser:
    browser = None  # Class-level attribute for Playwright browser instance
    playwright = None  # Class-level attribute for Playwright process

    @classmethod
    async def initialize_browser(cls):
        """
        Initialize the Playwright browser instance asynchronously.

        Example:
            await CustomBrowser.initialize_browser()
        """
        try:
            if cls.browser is None:
                if cls.playwright is None:
                    cls.playwright = await async_playwright().__aenter__()  # Initialize Playwright process
                    logger.info('playwright successfully initialized.')
                cls.browser = await cls.playwright.chromium.launch(headless=True)
                logger.info('Browser successfully initialized.')
        except Exception as e:
            logger.error(f'Failed to initialize browser: {e}')
