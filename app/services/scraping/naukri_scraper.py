import httpx
from typing import List
from datetime import datetime, timezone
from app.services.scraping.base import BaseJobScraper
from app.schemas.job import JobCreate

class NaukriScraper(BaseJobScraper):
    """
    Scraper for Naukri using their frontend API if possible, or a fallback.
    """
    
    @property
    def platform_name(self) -> str:
        return "Naukri"
        
    async def scrape(self, query: str = None, location: str = None) -> List[JobCreate]:
        # Using a simplified query approach for demonstration
        # Real Naukri scraping often needs complex headers
        query = query or "developer"
        location = location or "india"
        
        # This is a sample of how we'd call their internal API used by the frontend
        url = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword={query}&location={location}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Appid": "109",
            "Systemid": "109",
            "Clientid": "d3yc7",
        }
        
        try:
            async with httpx.AsyncClient(headers=headers, timeout=20.0) as client:
                response = await client.get(url)
                if response.status_code != 200:
                    print(f"Naukri Scraper: Failed with status {response.status_code}")
                    # If API fails, we could fallback to web scraping, but Naukri is dynamic.
                    # Returning empty for now to avoid blocking ScraperManager.
                    return []
                
                data = response.json()
                job_list = data.get("jobDetails", [])
                
                jobs = []
                for job in job_list:
                    try:
                        title = job.get("title")
                        company = job.get("companyName")
                        
                        if not title or not company:
                            continue
                            
                        # Extract location
                        loc = job.get("placeholders", [])
                        loc_val = "India"
                        for p in loc:
                            if p.get("type") == "location":
                                loc_val = p.get("label", "India")
                                break
                        
                        job_id = job.get("jobId")
                        apply_url = f"https://www.naukri.com/job-listings-{job_id}" if job_id else "https://www.naukri.com"
                        
                        job_data = {
                            "title": title,
                            "company": company,
                            "location": loc_val,
                            "apply_url": apply_url,
                            "description": job.get("jobDescription", ""),
                            "posted_date": datetime.now(timezone.utc),
                            "experience_level": job.get("experience"),
                            "salary_range": job.get("salary"),
                        }
                        
                        jobs.append(self.normalize_job(job_data))
                    except Exception as e:
                        print(f"Error parsing Naukri job: {e}")
                        continue
                        
                return jobs
                
        except Exception as e:
            print(f"Naukri Scraper Error: {e}")
            return []
