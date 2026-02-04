from abc import ABC, abstractmethod
from typing import List
from app.schemas.job import JobCreate


class BaseJobScraper(ABC):
    """
    Abstract base class for job scrapers.
    
    All job scrapers must implement the scrape() method
    to fetch and normalize job data from their respective platforms.
    """
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return the name of the platform being scraped"""
        pass
    
    @abstractmethod
    async def scrape(self, query: str = None, location: str = None) -> List[JobCreate]:
        """
        Scrape jobs from the platform.
        
        Args:
            query: Job search query (e.g., "Software Engineer")
            location: Location filter (e.g., "New York")
            
        Returns:
            List of normalized job data as JobCreate schemas
        """
        pass
    
    def normalize_job(self, raw_job: dict) -> JobCreate:
        """
        Normalize raw job data to JobCreate schema.
        Override this method to handle platform-specific data.
        """
        return JobCreate(
            title=raw_job.get("title", "Unknown"),
            company=raw_job.get("company", "Unknown"),
            location=raw_job.get("location"),
            platform=self.platform_name,
            description=raw_job.get("description"),
            apply_url=raw_job.get("apply_url"),
            posted_date=raw_job.get("posted_date"),
            experience_level=raw_job.get("experience_level"),
            salary_range=raw_job.get("salary_range"),
        )
