from fastapi import APIRouter
from typing import Any
from loguru import logger

from app.api.model.crawl_job_request import CrawlJobRequest
from app.api.model.crawl_job_response import CrawlJobResponse
from app.services.crawl_job_service import extract_ldjson_job

router = APIRouter()


@router.post(
    path="/crawljob",
    response_model=CrawlJobResponse,
    summary="crawl a job url and retrieve ls-json",
)
async def crawl_job(
        crawljobrequest: CrawlJobRequest
) -> Any:
    crawljobresponse = await extract_ldjson_job(crawljobrequest)

    logger.info("crawljobresponse '{response}'",
                response=crawljobresponse.jobViewUrl)

    return crawljobresponse
