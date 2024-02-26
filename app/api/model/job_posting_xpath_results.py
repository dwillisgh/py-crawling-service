from pydantic import BaseModel
from typing import Optional


class JobPostingXpathResults(BaseModel):
    xpath: Optional[str] = None
    jobPostingPropertyEnum: Optional[str] = None
    htmlElementValueTypeEnum: Optional[str] = None
    textOrHtml: Optional[str] = None


