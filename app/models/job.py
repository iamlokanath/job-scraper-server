from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255))
    platform = Column(String(100))  # e.g., LinkedIn, Indeed, Mock
    description = Column(Text)
    apply_url = Column(String(500))
    posted_date = Column(DateTime)
    experience_level = Column(String(50))  # e.g., Entry, Mid, Senior
    salary_range = Column(String(100))  # e.g., "$80k-$100k"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    applied_jobs = relationship("AppliedJob", back_populates="job")
