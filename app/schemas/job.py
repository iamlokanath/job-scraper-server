from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    platform: Optional[str] = None
    description: Optional[str] = None
    apply_url: Optional[str] = None
    posted_date: Optional[datetime] = None
    experience_level: Optional[str] = None
    salary_range: Optional[str] = None


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    jobs: list[JobResponse]
    total: int
