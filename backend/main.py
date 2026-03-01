import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import socketio
from routers import sessions, ai_agent, containers, tunnels
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(title="Ghost Labs Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.io setup
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Include routers
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(ai_agent.router, prefix="/api/ai", tags=["ai"])
app.include_router(containers.router, prefix="/api/containers", tags=["containers"])
app.include_router(tunnels.router, prefix="/api/tunnels", tags=["tunnels"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Ghost Labs Monolithic API is running"}

# Socket.io event handlers (basic scaffolding)
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on("join-session")
async def handle_join_session(sid, session_id):
    await sio.enter_room(sid, session_id)
    await sio.emit("user-joined", {"socketId": sid}, room=session_id, skip_sid=sid)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
