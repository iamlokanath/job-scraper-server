import httpx
from typing import List
from datetime import datetime, timezone
from app.services.scraping.base import BaseJobScraper
from app.schemas.job import JobCreate

class UnstopScraper(BaseJobScraper):
    """
    Scraper for Unstop Jobs using their public API.
    """
    
    @property
    def platform_name(self) -> str:
        return "Unstop"
        
    async def scrape(self, query: str = None, location: str = None) -> List[JobCreate]:
        # Unstop doesn't handle location well in their direct keyword search via API sometimes,
        # but let's try their public search API.
        query = query or "Software"
        
        url = f"https://unstop.com/api/public/opportunity/search-new?opportunity_type=jobs&per_page=12&page=1&keyword={query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://unstop.com/job",
        }
        
        try:
            async with httpx.AsyncClient(headers=headers, timeout=20.0) as client:
                response = await client.get(url)
                if response.status_code != 200:
                    print(f"Unstop Scraper: Failed. Status: {response.status_code}")
                    return []
                
                data = response.json()
                opportunities = data.get("data", {}).get("data", [])
                
                jobs = []
                for opp in opportunities:
                    try:
                        title = opp.get("title")
                        company = opp.get("organisation", {}).get("name")
                        
                        if not title or not company:
                            continue
                            
                        # Extract location
                        locations = opp.get("job_location", [])
                        loc_str = ", ".join(locations) if locations else "Remote/India"
                        
                        # Apply URL
                        slug = opp.get("public_url")
                        apply_url = f"https://unstop.com/o/{slug}" if slug else "https://unstop.com/job"
                        
                        job_data = {
                            "title": title,
                            "company": company,
                            "location": loc_str,
                            "apply_url": apply_url,
                            "description": opp.get("reg_status", "Open for applications"),
                            "posted_date": datetime.now(timezone.utc),
                            "experience_level": opp.get("filters", {}).get("experience_level", []),
                            "salary_range": opp.get("job_detail", {}).get("salary_range"),
                        }
                        
                        jobs.append(self.normalize_job(job_data))
                    except Exception as e:
                        print(f"Error parsing Unstop job: {e}")
                        continue
                        
                return jobs
                
        except Exception as e:
            print(f"Unstop Scraper Error: {e}")
            return []
        
