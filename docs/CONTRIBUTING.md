# Contributing to Ghost Labs

Thank you for your interest in contributing to Ghost Labs! This is an open-source project designed to help college students learn about real-time collaboration, containerization, and web development.

## 🎯 Project Overview

Ghost Labs is a secure collaborative workspace that provides:
- Real-time video/audio communication
- Persistent Linux lab environments in lightweight containers
- Collaborative code editing
- AI coding assistant
- Snapshot functionality to save and resume work

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Docker and Docker Compose
- Git
- Basic knowledge of JavaScript/React

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Ghost-Labs.git
   cd Ghost-Labs
   ```

2. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   cd ../backend
   npm install
   ```

4. **Install service dependencies**
   ```bash
   cd ../services/container-manager
   npm install
   
   cd ../ai-agent
   npm install
   ```

5. **Set up environment variables**
   ```bash
   # In backend directory
   cp .env.example .env
   
   # In services/container-manager
   cp .env.example .env
   
   # In services/ai-agent
   cp .env.example .env
   ```

6. **Build the workspace Docker image**
   ```bash
   cd ../..
   docker build -t ghost-labs-workspace:latest -f docker/workspace/Dockerfile docker/workspace
   ```

### Running the Project

**Option 1: Using Docker Compose (Recommended)**
```bash
docker-compose up
```

**Option 2: Running services individually**
```bash
# Terminal 1 - Backend
cd backend && npm run dev

# Terminal 2 - Frontend
cd frontend && npm run dev

# Terminal 3 - Container Manager
cd services/container-manager && npm run dev

# Terminal 4 - AI Agent
cd services/ai-agent && npm run dev
```

## 📋 Available Issues for Beginners

Here are 12 beginner-friendly tasks to get started with Ghost Labs:

### Issue 1: Integrate xterm.js for Terminal Emulator
**Difficulty:** Easy  
**Skills:** JavaScript, React  
**Description:**  
The Terminal component currently shows a placeholder. Integrate xterm.js library to create a functional terminal emulator that can display text and handle user input.

**Tasks:**
- Import xterm.js and xterm-addon-fit in `frontend/src/components/Terminal.tsx`
- Initialize the terminal in the useEffect hook
- Set up terminal styling (dark theme)
- Make the terminal fit the container using FitAddon

**Resources:**
- [xterm.js documentation](https://xtermjs.org/)

---

### Issue 2: Integrate Monaco Editor for Code Editing
**Difficulty:** Easy  
**Skills:** JavaScript, React  
**Description:**  
Replace the placeholder in CodeEditor component with Microsoft's Monaco Editor (the editor used in VS Code).

**Tasks:**
- Use `@monaco-editor/react` package (already in package.json)
- Set up Monaco editor with VS Code dark theme
- Handle file content loading
- Add language detection based on file extension

**Resources:**
- [Monaco Editor React documentation](https://github.com/suren-atoyan/monaco-react)

---

### Issue 3: Implement File Tree Component
**Difficulty:** Medium  
**Skills:** JavaScript, React, Recursion  
**Description:**  
The FileExplorer component currently shows a flat list. Implement a proper file tree that supports nested folders.

**Tasks:**
- Create recursive tree rendering for folders and files
- Add expand/collapse functionality for folders
- Show appropriate icons for files and folders
- Connect to backend API to fetch actual file structure

**File:** `frontend/src/components/FileExplorer.tsx`

---

### Issue 4: Add WebRTC Video/Audio Communication
**Difficulty:** Medium  
**Skills:** JavaScript, WebRTC  
**Description:**  
Implement basic WebRTC functionality for peer-to-peer video/audio calls between participants.

**Tasks:**
- Request camera/microphone permissions
- Create peer connections using RTCPeerConnection
- Use the existing Socket.io signaling (already set up in backend)
- Display local and remote video streams
- Add mute/unmute buttons

**File:** `frontend/src/components/VideoCall.tsx`

**Resources:**
- [WebRTC documentation](https://webrtc.org/getting-started/overview)

---

### Issue 5: Connect Terminal to Container via WebSocket
**Difficulty:** Medium  
**Skills:** JavaScript, WebSockets, Docker  
**Description:**  
Create a real-time connection between the frontend terminal and the Docker container terminal.

**Tasks:**
- Set up WebSocket event handlers in Terminal component
- Emit terminal input to backend via Socket.io
- Receive terminal output from backend
- Connect backend to container's stdin/stdout using dockerode
- Handle terminal resize events

**Files:** 
- `frontend/src/components/Terminal.tsx`
- `backend/src/socket/index.js`
- `services/container-manager/src/index.js`

---

### Issue 6: Implement User Authentication (Basic)
**Difficulty:** Easy  
**Skills:** JavaScript, JWT, Express  
**Description:**  
Add basic JWT-based authentication for users joining sessions.

**Tasks:**
- Create login/signup forms on homepage
- Implement JWT token generation on backend
- Add middleware to verify JWT tokens
- Store user info in session
- Add username display in workspace header

**Files:**
- `backend/src/routes/auth.js` (new file)
- `frontend/src/pages/HomePage.tsx`

**Resources:**
- [JWT documentation](https://jwt.io/)

---

### Issue 7: Create Snapshot Save/Restore UI
**Difficulty:** Medium  
**Skills:** JavaScript, React, REST API  
**Description:**  
Build the UI for saving and restoring container snapshots.

**Tasks:**
- Create a modal/sidebar for snapshot management
- List existing snapshots
- Add form to create new snapshot with name and description
- Implement restore snapshot functionality
- Connect to container-manager API endpoints
- Show loading states during snapshot operations

**File:** Create `frontend/src/components/SnapshotManager.tsx`

---

### Issue 8: Add Simple Chat Feature
**Difficulty:** Easy  
**Skills:** JavaScript, React, Socket.io  
**Description:**  
Add a text chat feature so participants can communicate without using voice.

**Tasks:**
- Create a Chat component (similar to AIAssistant)
- Add Socket.io events for sending/receiving messages
- Show message history
- Display username with each message
- Add timestamp to messages

**File:** Create `frontend/src/components/Chat.tsx`

---

### Issue 9: Integrate OpenAI API for AI Assistant
**Difficulty:** Medium  
**Skills:** JavaScript, REST API, OpenAI API  
**Description:**  
Connect the AI Assistant to OpenAI's API for actual code suggestions.

**Tasks:**
- Set up OpenAI API key in environment variables
- Implement chat completion API call in ai-agent service
- Handle streaming responses
- Add context from current file being edited
- Implement error handling for API failures

**File:** `services/ai-agent/src/index.js`

**Resources:**
- [OpenAI API documentation](https://platform.openai.com/docs)

---

### Issue 11: Build and Test OS Images
**Difficulty:** Easy  
**Skills:** Docker, Bash  
**Description:**  
Build all available OS images and create a test script to verify they work correctly.

**Tasks:**
- Run the build-all.sh script in docker/os-images
- Test each OS image by creating a container
- Verify basic tools are installed (git, vim, node, python)
- Create a test script that validates OS images
- Document any build errors or issues

**File:** `docker/os-images/build-all.sh`

---

### Issue 12: Test Cloudflared Tunnel Creation
**Difficulty:** Medium  
**Skills:** Node.js, Networking  
**Description:**  
Test the tunnel manager service and improve error handling and logging.

**Tasks:**
- Install cloudflared on your system
- Start the tunnel manager service
- Test tunnel creation with curl/Postman
- Test tunnel closing and cleanup
- Add better error messages
- Add timeout handling
- Test with multiple simultaneous tunnels

**File:** `services/tunnel-manager/src/index.js`

**Resources:**
- [Cloudflared documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps)

---

### Issue 10: Add Database Integration with SQLite
**Difficulty:** Medium  
**Skills:** JavaScript, SQL, Database Design  
**Description:**  
Replace in-memory storage with SQLite database for persistent data.

**Tasks:**
- Set up better-sqlite3 (already in package.json)
- Create database schema for users, sessions, snapshots
- Create database initialization script
- Update session routes to use database
- Add migration system for schema changes

**Files:**
- Create `backend/src/db/schema.sql`
- Create `backend/src/db/index.js`
- Update `backend/src/routes/session.js`

---

## 🔧 Development Guidelines

### Code Style

- Use meaningful variable and function names
- Add comments for complex logic
- Follow existing code formatting
- Use ES6+ features (arrow functions, async/await, etc.)

### Git Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/issue-name`
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages: `git commit -m "Add: feature description"`
6. Push to your fork: `git push origin feature/issue-name`
7. Create a Pull Request

### Commit Message Format

- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for updates to existing features
- `Docs:` for documentation changes
- `Style:` for formatting changes

### Testing

Before submitting a PR:
- Test your changes locally
- Ensure no console errors
- Check that existing features still work
- Test on different screen sizes (for UI changes)

## 📚 Resources

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [React Documentation](https://react.dev/)
- [Express.js Documentation](https://expressjs.com/)
- [Socket.io Documentation](https://socket.io/)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Getting Help

- Open an issue for bugs or questions
- Comment on an issue before starting work
- Join discussions in existing issues
- Ask questions in pull requests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy Coding! 🚀**
