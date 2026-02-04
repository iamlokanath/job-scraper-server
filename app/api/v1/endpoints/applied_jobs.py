from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.job import Job
from app.models.applied_job import AppliedJob
from app.schemas.applied_job import (
    AppliedJobCreate,
    AppliedJobResponse,
    AppliedJobListResponse,
)

router = APIRouter(prefix="/applied-jobs", tags=["Applied Jobs"])


@router.get("", response_model=AppliedJobListResponse)
async def list_applied_jobs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    List all jobs the current user has applied to.
    """
    user_id = int(current_user["user_id"])
    
    applied_jobs = (
        db.query(AppliedJob)
        .filter(AppliedJob.user_id == user_id)
        .order_by(AppliedJob.applied_at.desc())
        .all()
    )
    
    return AppliedJobListResponse(
        applied_jobs=applied_jobs,
        total=len(applied_jobs)
    )


@router.post("", response_model=AppliedJobResponse, status_code=status.HTTP_201_CREATED)
async def apply_to_job(
    request: AppliedJobCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Apply to a job. Records the application in the database.
    """
    user_id = int(current_user["user_id"])
    
    # Check if job exists
    job = db.query(Job).filter(Job.id == request.job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check if already applied
    existing = db.query(AppliedJob).filter(
        AppliedJob.user_id == user_id,
        AppliedJob.job_id == request.job_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied to this job"
        )
    
    # Create application
    applied_job = AppliedJob(
        user_id=user_id,
        job_id=request.job_id
    )
    
    db.add(applied_job)
    db.commit()
    db.refresh(applied_job)
    
    return applied_job


@router.delete("/{applied_job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_application(
    applied_job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Remove a job application.
    """
    user_id = int(current_user["user_id"])
    
    applied_job = db.query(AppliedJob).filter(
        AppliedJob.id == applied_job_id,
        AppliedJob.user_id == user_id
    ).first()
    
    if not applied_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    db.delete(applied_job)
    db.commit()
