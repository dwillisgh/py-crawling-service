from pydantic import BaseModel
from typing import Optional

from app.api.model.job_posting_xpath_definitions import JobPostingXpathDefinitions


class CrawlJobRequest(BaseModel):
    jobViewUrl: Optional[str] = None
    jobPostingXpathDefinitions: Optional[JobPostingXpathDefinitions] = None
