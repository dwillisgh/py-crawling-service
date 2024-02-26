from pydantic import BaseModel
from typing import Optional, List

from app.api.model.job_posting_xpath_results import JobPostingXpathResults


class CrawlJobResponse(BaseModel):
    jobViewUrl: Optional[str] = None
    rawLdJsons: Optional[str] = None
    status: Optional[int] = None
    jobPostingXpathResults: Optional[List[JobPostingXpathResults]] = None
