from loguru import logger
from lxml import html
from playwright.async_api import async_playwright
from lxml.html.soupparser import fromstring, etree

from app.api.model.crawl_job_response import CrawlJobResponse
from app.api.model.job_posting_xpath_results import JobPostingXpathResults

browser = None  # global attribute for Playwright browser instance
playwright = None  # global attribute for Playwright process


async def initialize_browser():
    try:
        global browser
        if browser is None:
            global playwright
            if playwright is None:
                playwright = await async_playwright().__aenter__()  # Initialize Playwright process
                logger.info('playwright successfully initialized.')
            browser = await playwright.chromium.launch(headless=True)
            logger.info('Browser successfully initialized.')
    except Exception as e:
        logger.error(f'Failed to initialize browser: {e}')


async def extract_xpaths(tree, crawljobrequest):
    if crawljobrequest.jobPostingXpathDefinitions is None:
        return None
    if crawljobrequest.jobPostingXpathDefinitions.jobPostingXpaths is None:
        return None

    jobpostingxpathresultslist = []

    for jobpostingxpath in crawljobrequest.jobPostingXpathDefinitions.jobPostingXpaths:
        xpath_elements = tree.xpath(jobpostingxpath.xpath)
        if xpath_elements is None:
            continue

        jobpostingxpathresults = JobPostingXpathResults()
        textorhtml = ""
        for xpath_element in xpath_elements:
            if jobpostingxpath.htmlElementValueTypeEnum == "HTML":
                res = etree.tostring(xpath_element)
                textorhtml += res.decode("utf-8")
            else:
                if xpath_element.text_content() is not None:
                    textorhtml += xpath_element.text_content()

        jobpostingxpathresults.textOrHtml = textorhtml
        jobpostingxpathresults.xpath = jobpostingxpath.xpath
        jobpostingxpathresults.jobPostingPropertyEnum = jobpostingxpath.jobPostingPropertyEnum
        jobpostingxpathresults.htmlElementValueTypeEnum = jobpostingxpath.htmlElementValueTypeEnum
        jobpostingxpathresultslist.append(jobpostingxpathresults)

    return jobpostingxpathresultslist


async def extract_ldjson_job(crawljobrequest):
    global browser

    # init the global browser
    await initialize_browser()

    # Open a new browser page
    context = await browser.new_context()

    page = None
    try:
        page = await context.new_page()
        response = await page.goto(crawljobrequest.jobViewUrl)
        crawljobresponse = CrawlJobResponse()
        crawljobresponse.status = response.status
        # await page.wait_for_load_state("networkidle")

        content = await page.content()
        tree = fromstring(content)

        ld_json_elements = tree.xpath('//script[@type="application/ld+json"]')

        if ld_json_elements is not None:
            for ld_json_element in ld_json_elements:
                if "JobPosting" in ld_json_element.text:
                    crawljobresponse.rawLdJsons = ld_json_element.text

        # extract any xpaths
        crawljobresponse.jobPostingXpathResults = await extract_xpaths(tree,
                                                                       crawljobrequest)

        crawljobresponse.jobViewUrl = crawljobrequest.jobViewUrl

        return crawljobresponse

    finally:
        await page.close()
        await context.close()
