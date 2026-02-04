from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobResponse, JobListResponse, JobCreate
from app.services.scraping import ScraperManager

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=JobListResponse)
async def list_jobs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    query: Optional[str] = None,
    location: Optional[str] = None,
):
    """
    List all available jobs with pagination.
    """
    jobs_query = db.query(Job)
    
    # Filter by title/company if query provided
    if query:
        jobs_query = jobs_query.filter(
            (Job.title.ilike(f"%{query}%")) | 
            (Job.company.ilike(f"%{query}%"))
        )
    
    # Filter by location if provided
    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f"%{location}%"))
    
    total = jobs_query.count()
    jobs = jobs_query.order_by(Job.posted_date.desc()).offset(skip).limit(limit).all()
    
    return JobListResponse(jobs=jobs, total=total)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get a specific job by ID.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job


@router.post("/scrape", response_model=JobListResponse)
async def scrape_jobs(
    db: Session = Depends(get_db),
    query: Optional[str] = None,
    location: Optional[str] = None,
):
    """
    Trigger job scraping and store results in database.
    Aggregates jobs from multiple platforms.
    """
    manager = ScraperManager()
    scraped_jobs = await manager.scrape_all(query=query, location=location)
    
    new_jobs_count = 0
    created_jobs = []
    
    for job_data in scraped_jobs:
        # Check if job already exists (simplified check by title, company, and location)
        existing = db.query(Job).filter(
            Job.title == job_data.title,
            Job.company == job_data.company,
            Job.location == job_data.location
        ).first()
        
        if not existing:
            job = Job(**job_data.model_dump())
            db.add(job)
            created_jobs.append(job)
            new_jobs_count += 1
    
    db.commit()
    
    # Refresh to get IDs
    for job in created_jobs:
        db.refresh(job)
    
    return JobListResponse(jobs=created_jobs, total=new_jobs_count)
