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

class CreateSnapshotRequest(BaseModel):
    name: str
    description: Optional[str] = ""


# --- Static routes MUST come before /{session_id} to avoid path conflicts ---

@router.post("/create")
async def create_session(req: CreateSessionRequest, db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())

    db_session = models.Session(
        id=session_id,
        os_type=req.osType,
        snapshot_id=req.snapshotId,
        container_id="mock-container-id",
        tunnel_url="http://mock-tunnel.url",
    )
    db.add(db_session)

    db_participant = models.Participant(
        session_id=session_id,
        user_id=req.userId,
        username=req.username,
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
        ],
    }


@router.get("/snapshots")
async def list_all_snapshots(db: Session = Depends(get_db)):
    snapshots = db.query(models.Snapshot).order_by(models.Snapshot.created_at.desc()).all()
    return {
        "success": True,
        "snapshots": [
            {
                "id": s.id,
                "sessionId": s.session_id,
                "name": s.name,
                "description": s.description,
                "createdAt": s.created_at.isoformat() if s.created_at else None,
                "containerId": s.container_id,
                "osType": s.os_type,
            }
            for s in snapshots
        ],
    }


# --- Dynamic routes with {session_id} ---

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
        username=participant.username,
    )
    db.add(db_participant)
    db.commit()

    db.refresh(db_session)
    return {"success": True, "session": db_session}


@router.get("/{session_id}/snapshots")
async def list_session_snapshots(session_id: str, db: Session = Depends(get_db)):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    snapshots = (
        db.query(models.Snapshot)
        .filter(models.Snapshot.session_id == session_id)
        .order_by(models.Snapshot.created_at.desc())
        .all()
    )
    return {
        "success": True,
        "snapshots": [
            {
                "id": s.id,
                "sessionId": s.session_id,
                "name": s.name,
                "description": s.description,
                "createdAt": s.created_at.isoformat() if s.created_at else None,
                "containerId": s.container_id,
                "osType": s.os_type,
            }
            for s in snapshots
        ],
    }


@router.post("/{session_id}/snapshots")
async def create_snapshot(session_id: str, req: CreateSnapshotRequest, db: Session = Depends(get_db)):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    snapshot = models.Snapshot(
        session_id=session_id,
        name=req.name,
        description=req.description or "",
        container_id=db_session.container_id,
        os_type=db_session.os_type,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return {
        "success": True,
        "snapshot": {
            "id": snapshot.id,
            "sessionId": snapshot.session_id,
            "name": snapshot.name,
            "description": snapshot.description,
            "createdAt": snapshot.created_at.isoformat() if snapshot.created_at else None,
            "containerId": snapshot.container_id,
            "osType": snapshot.os_type,
        },
    }


@router.post("/{session_id}/snapshots/{snapshot_id}/restore")
async def restore_snapshot(session_id: str, snapshot_id: str, db: Session = Depends(get_db)):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    snapshot = (
        db.query(models.Snapshot)
        .filter(models.Snapshot.id == snapshot_id, models.Snapshot.session_id == session_id)
        .first()
    )
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    db_session.snapshot_id = snapshot.id
    db.commit()
    db.refresh(db_session)

    return {
        "success": True,
        "message": f"Restored snapshot '{snapshot.name}' successfully",
        "session": {
            "id": db_session.id,
            "snapshotId": db_session.snapshot_id,
            "containerId": db_session.container_id,
            "osType": db_session.os_type,
        },
    }
