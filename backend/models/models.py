from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    container_id = Column(String, nullable=True)
    tunnel_url = Column(String, nullable=True)
    os_type = Column(String, default="alpine")
    snapshot_id = Column(String, nullable=True)

    participants = relationship("Participant", back_populates="session")
    snapshots = relationship("Snapshot", back_populates="session")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    joined_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("Session", back_populates="participants")


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    container_id = Column(String, nullable=True)
    os_type = Column(String, nullable=True)

    session = relationship("Session", back_populates="snapshots")
