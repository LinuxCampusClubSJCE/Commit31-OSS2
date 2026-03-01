from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from typing import List, Optional, Any
import datetime

from database import get_db
import models

router = APIRouter()

class ParticipantBase(BaseModel):
    userId: str
    username: str

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    joinedAt: datetime.datetime

    class Config:
        from_attributes = True

class SessionSchema(BaseModel):
    id: str
    createdAt: datetime.datetime
    participants: List[Participant]
    containerId: Optional[str] = None
    tunnelUrl: Optional[str] = None
    osType: str
    snapshotId: Optional[str] = None

    class Config:
        from_attributes = True

class CreateSessionRequest(BaseModel):
    osType: Optional[str] = "alpine"
    snapshotId: Optional[str] = None
    userId: str
    username: str

@router.post("/create")
async def create_session(req: CreateSessionRequest, db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    
    # Create new session record
    db_session = models.Session(
        id=session_id,
        os_type=req.osType,
        snapshot_id=req.snapshotId,
        container_id="mock-container-id", # Placeholder
        tunnel_url="http://mock-tunnel.url" # Placeholder
    )
    db.add(db_session)
    
    # Add creator as a participant
    db_participant = models.Participant(
        session_id=session_id,
        user_id=req.userId,
        username=req.username
    )
    db.add(db_participant)
    
    db.commit()
    db.refresh(db_session)
    
    return {"success": True, "session": db_session}

@router.get("/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True, "session": db_session}

@router.post("/{session_id}/join")
async def join_session(session_id: str, participant: ParticipantCreate, db: Session = Depends(get_db)):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_participant = models.Participant(
        session_id=session_id,
        user_id=participant.userId,
        username=participant.username
    )
    db.add(db_participant)
    db.commit()
    
    db.refresh(db_session)
    return {"success": True, "session": db_session}

@router.get("/os-options")
async def get_os_options():
    return {
        "success": True,
        "osOptions": [
            {"id": "alpine", "name": "Alpine Linux", "description": "Lightweight (~5MB)", "icon": "🏔️"},
            {"id": "ubuntu", "name": "Ubuntu 22.04", "description": "Popular & Beginner-friendly", "icon": "🟠"},
            {"id": "debian", "name": "Debian 12", "description": "Stable & Reliable", "icon": "🔴"},
            {"id": "fedora", "name": "Fedora 39", "description": "Modern & Cutting-edge", "icon": "🔵"},
            {"id": "arch", "name": "Arch Linux", "description": "Rolling Release", "icon": "⚫"},
        ]
    }
