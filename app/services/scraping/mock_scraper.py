from typing import List
from datetime import datetime, timezone, timedelta
from app.services.scraping.base import BaseJobScraper
from app.schemas.job import JobCreate


class MockJobScraper(BaseJobScraper):
    """
    Mock job scraper that returns sample job data.
    Used for development and testing purposes.
    """
    
    @property
    def platform_name(self) -> str:
        return "MockPlatform"
    
    async def scrape(self, query: str = None, location: str = None) -> List[JobCreate]:
        """Return sample mock job data"""
        
        # Sample jobs for demonstration
        mock_jobs = [
            {
                "title": "Senior Software Engineer",
                "company": "TechCorp Inc.",
                "location": "San Francisco, CA",
                "description": "We are looking for a Senior Software Engineer to join our team. You will work on cutting-edge technologies and help build scalable systems.",
                "apply_url": "https://example.com/jobs/1",
                "posted_date": datetime.now(timezone.utc) - timedelta(days=2),
                "experience_level": "Senior",
                "salary_range": "$150k - $200k",
            },
            {
                "title": "Full Stack Developer",
                "company": "StartupXYZ",
                "location": "New York, NY",
                "description": "Join our fast-growing startup as a Full Stack Developer. Work with React, Node.js, and PostgreSQL.",
                "apply_url": "https://example.com/jobs/2",
                "posted_date": datetime.now(timezone.utc) - timedelta(days=1),
                "experience_level": "Mid",
                "salary_range": "$100k - $140k",
            },
            {
                "title": "Backend Engineer",
                "company": "DataFlow Systems",
                "location": "Remote",
                "description": "Build robust backend systems using Python and FastAPI. Experience with microservices architecture is a plus.",
                "apply_url": "https://example.com/jobs/3",
                "posted_date": datetime.now(timezone.utc),
                "experience_level": "Mid",
                "salary_range": "$120k - $160k",
            },
            {
                "title": "Junior Frontend Developer",
                "company": "WebAgency",
                "location": "Austin, TX",
                "description": "Great opportunity for entry-level developers to learn and grow. You will work with React and TypeScript.",
                "apply_url": "https://example.com/jobs/4",
                "posted_date": datetime.now(timezone.utc) - timedelta(days=3),
                "experience_level": "Entry",
                "salary_range": "$60k - $80k",
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudNative Ltd.",
                "location": "Seattle, WA",
                "description": "Manage cloud infrastructure on AWS and implement CI/CD pipelines. Kubernetes experience required.",
                "apply_url": "https://example.com/jobs/5",
                "posted_date": datetime.now(timezone.utc) - timedelta(days=5),
                "experience_level": "Senior",
                "salary_range": "$140k - $180k",
            },
        ]
        
        # Filter by query if provided
        if query:
            query_lower = query.lower()
            mock_jobs = [
                job for job in mock_jobs 
                if query_lower in job["title"].lower() or query_lower in job["description"].lower()
            ]
        
        # Filter by location if provided
        if location:
            location_lower = location.lower()
            mock_jobs = [
                job for job in mock_jobs 
                if location_lower in job["location"].lower()
            ]
        
        return [self.normalize_job(job) for job in mock_jobs]
