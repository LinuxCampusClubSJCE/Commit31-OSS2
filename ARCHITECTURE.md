# Ghost Labs Architecture

## Overview
Ghost Labs is a secure collaborative workspace platform that provides:
- Real-time video/audio communication via WebRTC
- Persistent Linux lab environments for each user with multiple OS options
- Collaborative access to lab environments via temporary cloudflared tunnels
- Snapshot functionality for saving and resuming work
- AI coding assistant integrated into the workspace

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  (React + WebRTC + Monaco Editor + WebSocket Client)        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ WebSocket + REST API (Port 8000)
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                      FastAPI Monolith                        │
│             (Python + FastAPI + Socket.io)                   │
└─────┬──────────────┬──────────────┬─────────────────────────┘
      │              │              │
      │              │              │
┌─────▼─────┐  ┌────▼──────┐  ┌────▼──────────┐
│  Session  │  │Container  │  │  AI Agent     │
│  Router   │  │  Router   │  │  Router       │
└───────────┘  └─────┬─────┘  └───────────────┘
                     │
              ┌──────▼──────┐
              │   Docker    │
              │ Containers  │
              │(Linux Labs) │
              └─────────────┘
```

## Core Components

### 1. Frontend (`/frontend`)
- **Technology**: React, TypeScript, WebRTC, Socket.io-client
- **Features**:
  - Video call interface
  - Terminal emulator (xterm.js)
  - Code editor (Monaco Editor)
  - File browser
  - Snapshot management UI

### 2. Monolithic Backend (`/backend`)
- **Technology**: Python 3.11, FastAPI, python-socketio
- **Responsibilities**:
  - WebSocket connection management
  - User authentication (planned)
  - Session management
  - Container lifecycle management (Docker SDK)
  - Tunnel management (cloudflared)
  - AI Agent integration

## Data Flow

### User Creates Session
1. User selects OS type or snapshot on homepage
2. User enters name and clicks "Create New Session"
3. Backend creates container with selected OS via Docker SDK
4. Backend creates cloudflared tunnel
5. Tunnel URL is generated (e.g., https://xyz.trycloudflare.com)
6. WebSocket connection established
7. User redirected to workspace with tunnel URL

### Collaborative Access
1. User A shares screen/terminal with User B
2. WebSocket broadcasts terminal output to all participants
3. Input from any user forwarded to container
4. Changes synchronized in real-time

## Technology Stack

### Frontend
- React 18
- TypeScript
- Socket.io-client
- xterm.js (terminal emulator)
- Monaco Editor (code editor)
- WebRTC (video/audio)

### Backend
- Python 3.11
- FastAPI
- python-socketio
- Docker SDK for Python
- SQLite (planned)

### Infrastructure
- Docker (containerization)
- Multiple Linux distributions (Alpine, Ubuntu, Debian, Fedora, Arch)
- cloudflared (secure tunneling)

## Security Considerations

1. **Container Isolation**: Each lab runs in isolated Docker container
2. **Resource Limits**: CPU, memory, disk limits per container
3. **Network Isolation**: Containers have limited network access
4. **Authentication**: JWT-based auth (planned)
5. **Input Validation**: Sanitize all user inputs
