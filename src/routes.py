"""
routes.py

This file contains the route definitions for the User Management API.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
import datetime

from src.auth import verify_token
from src.database import get_db
from src.models import AuditLog, UserActivitySummary
from src.schemas import ActivitySummarizationRequest, SummaryOutput
from src.summarizer import generate_summary

router = APIRouter()

@router.post("/ai/summarize-user-activity", response_model=SummaryOutput, status_code=status.HTTP_201_CREATED)
def summarize_user_activity(request: ActivitySummarizationRequest, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    """
    Endpoint to generate natural language summaries of user actions from the AuditLog.
    
    Args:
        request (ActivitySummarizationRequest): The request containing user ID and time range for activity.
        db (Session): Database session dependency.
        token (str, optional): JWT token for authentication. Defaults to Depends(verify_token).
        
    Returns:
        SummaryOutput: The generated summary of the user's activities.
    
    Raises:
        HTTPException 404: If no audit logs are found for the given user ID and time range.
    """
    start_time = request.start_time
    end_time = request.end_time
    user_id = request.user_id

    # Query the database for activity logs within the specified time range
    activity_logs = db.query(AuditLog).filter(
        AuditLog.user_id == user_id,
        AuditLog.timestamp >= start_time,
        AuditLog.timestamp <= end_time
    ).all()

    if not activity_logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No activity logs found for the given time range.")

    # Generate a summary of the activity logs
    summary = generate_summary([log.activity for log in activity_logs])

    # Create a UserActivitySummary instance and save it to the database
    new_summary = UserActivitySummary(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        summary=summary
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    return JSONResponse(content={"message": "User activity summary generated successfully", "summary": new_summary.summary}, status_code=status.HTTP_201_CREATED)