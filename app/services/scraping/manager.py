from typing import List
import asyncio
from app.services.scraping.base import BaseJobScraper
from app.schemas.job import JobCreate
from app.services.scraping.mock_scraper import MockJobScraper
from app.services.scraping.linkedin_scraper import LinkedInScraper
from app.services.scraping.naukri_scraper import NaukriScraper
from app.services.scraping.unstop_scraper import UnstopScraper

class ScraperManager:
    """
    Manager to coordinate multiple job scrapers.
    """
    
    def __init__(self):
        self.scrapers: List[BaseJobScraper] = [
            LinkedInScraper(),
            NaukriScraper(),
            UnstopScraper()
        ]
    
    def add_scraper(self, scraper: BaseJobScraper):
        self.scrapers.append(scraper)
    
    async def scrape_all(self, query: str = None, location: str = None) -> List[JobCreate]:
        """
        Run all registered scrapers in parallel and aggregate results.
        """
        if not self.scrapers:
            # Fallback to mock if no real scrapers allowed or available
            mock = MockJobScraper()
            return await mock.scrape(query, location)
            
        # Run real scrapers in parallel
        tasks = [scraper.scrape(query, location) for scraper in self.scrapers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        aggregated_jobs = []
        for i, result in enumerate(results):
            scraper_name = self.scrapers[i].platform_name
            if isinstance(result, list):
                if result:
                    print(f"Scraper {scraper_name}: Found {len(result)} jobs")
                    aggregated_jobs.extend(result)
                else:
                    print(f"Scraper {scraper_name}: No jobs found")
            elif isinstance(result, Exception):
                print(f"Scraper {scraper_name} error: {result}")
                
        # If all real scrapers failed or found nothing, maybe use mock as a survival strategy 
        # (optional, but let's keep it real for now)
        if not aggregated_jobs:
            print("No real jobs found, using mock as fallback for demonstration")
            mock = MockJobScraper()
            return await mock.scrape(query, location)
            
        return aggregated_jobs
