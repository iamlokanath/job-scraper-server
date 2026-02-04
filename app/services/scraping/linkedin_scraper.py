import httpx
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime, timezone
import asyncio
from app.services.scraping.base import BaseJobScraper
from app.schemas.job import JobCreate

class LinkedInScraper(BaseJobScraper):
    """
    Scraper for LinkedIn Jobs (Public Search).
    """
    
    @property
    def platform_name(self) -> str:
        return "LinkedIn"
        
    async def scrape(self, query: str = None, location: str = None) -> List[JobCreate]:
        query = query or "Software Engineer"
        location = location or "India"
        
        # LinkedIn public search URL
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={query}&location={location}&start=0"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        try:
            async with httpx.AsyncClient(headers=headers, timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url)
                if response.status_code != 200:
                    print(f"LinkedIn Scraper: Failed to fetch jobs. Status: {response.status_code}")
                    return []
                
                soup = BeautifulSoup(response.text, "lxml")
                job_cards = soup.find_all("li")
                
                jobs = []
                for card in job_cards:
                    try:
                        title_tag = card.find("h3", class_="base-search-card__title")
                        company_tag = card.find("h4", class_="base-search-card__subtitle")
                        location_tag = card.find("span", class_="job-search-card__location")
                        link_tag = card.find("a", class_="base-card__full-link")
                        date_tag = card.find("time", class_="job-search-card__listdate")
                        
                        if not title_tag or not company_tag:
                            continue
                            
                        job_data = {
                            "title": title_tag.get_text(strip=True),
                            "company": company_tag.get_text(strip=True),
                            "location": location_tag.get_text(strip=True) if location_tag else location,
                            "apply_url": link_tag["href"] if link_tag else None,
                            "description": f"Job at {company_tag.get_text(strip=True)} on LinkedIn",
                            "posted_date": datetime.now(timezone.utc), # Simple fallback
                            "platform": self.platform_name
                        }
                        
                        jobs.append(self.normalize_job(job_data))
                    except Exception as e:
                        print(f"Error parsing LinkedIn job: {e}")
                        continue
                        
                return jobs
                
        except Exception as e:
            print(f"LinkedIn Scraper Error: {e}")
            return []
