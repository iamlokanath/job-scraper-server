from pydantic import BaseModel
from datetime import datetime
from app.schemas.job import JobResponse


class AppliedJobBase(BaseModel):
    job_id: int


class AppliedJobCreate(AppliedJobBase):
    pass


class AppliedJobResponse(BaseModel):
    id: int
    job_id: int
    applied_at: datetime
    job: JobResponse

    class Config:
        from_attributes = True


class AppliedJobListResponse(BaseModel):
    applied_jobs: list[AppliedJobResponse]
    total: int
