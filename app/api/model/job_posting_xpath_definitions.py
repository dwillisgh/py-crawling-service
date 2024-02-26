from pydantic import BaseModel
from typing import Optional, List


class JobPostingXpaths(BaseModel):
    xpath: Optional[str] = None
    jobPostingPropertyEnum: Optional[str] = None
    overwriteLdJson: Optional[bool] = None
    htmlElementValueTypeEnum: Optional[str] = None
    overwriteNullOrEmptyOnly: Optional[bool] = None


class JobPostingXpathDefinitions(BaseModel):
    jobPostingXpaths: Optional[List[JobPostingXpaths]] = None



