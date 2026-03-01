# 🚀 Ghost Labs

<p align="center">
  <img src="Commit31.png" alt="Ghost Labs Banner" width="800"/>
</p>

## Secure Collaborative Workspace with Persistent Linux Labs + AI Agent

Ghost Labs is an open-source platform that provides real-time collaborative workspaces with persistent Linux environments, designed to help students learn programming and collaboration skills.

### ✨ Features

- **🖥️ Persistent Linux Labs**: Lightweight Docker containers with multiple OS options (Alpine, Ubuntu, Debian, Fedora, Arch)
- **🤝 Real-time Collaboration**: Share and access workspaces together via WebSocket
- **🌐 Secure Tunnel Access**: Automatic cloudflared tunnel creation for each session
- **🎥 Video Communication**: Built-in WebRTC video/audio calls
- **💻 Code Editor**: Monaco Editor integration (VS Code editor)
- **🖥️ Terminal Access**: Full terminal access via xterm.js
- **💾 Snapshots**: Save and restore workspace states
- **🤖 AI Assistant**: Coding help powered by AI (OpenAI integration ready)

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐
│   Frontend  │────▶│   Backend    │
│   (React)   │     │  (FastAPI)   │
└─────────────┘     └──────────────┘
                           │
                           ├──────────▶ Docker Containers
                           │            (Linux Labs)
                           │
                           └──────────▶ Cloudflared Tunnels
                                        (Public Access)
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Ghost-Labs.git
   cd Ghost-Labs
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Manual Setup (Development)

If you prefer to run services individually:

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:socket_app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
Ghost-Labs/
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/          # Page components
│   │   └── hooks/          # Custom hooks
│   └── package.json
├── backend/                 # FastAPI monolithic backend
│   ├── main.py              # Entry point & Socket.io
│   ├── routers/             # API routes (sessions, ai, containers, tunnels)
│   └── requirements.txt
├── docker/
│   ├── os-images/          # Multiple OS Dockerfiles
│   └── workspace/          # Default Alpine workspace
├── docs/                    # Documentation files
│   ├── ARCHITECTURE.md     # Architecture documentation
│   ├── CONTRIBUTING.md     # Contribution guidelines
│   ├── CLOUDFLARED_IMPLEMENTATION.md
│   ├── PROJECT_SUMMARY.md
│   └── SETUP.md
└── docker-compose.yml
```

## 🎯 Use Cases

- **Programming Education**: Teachers create sessions, students join via tunnel URL
- **Team Collaboration**: Developers pair program in real-time with OS choice
- **Code Reviews**: Review code together with live discussions
- **Workshops**: Conduct hands-on programming workshops with persistent environments
- **Interview Practice**: Technical interview preparation with snapshot save/resume

## 🛠️ Technology Stack

### Frontend
- React 18
- TypeScript
- Socket.io-client
- xterm.js (terminal)
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

## 🤝 Contributing

We welcome contributions from developers of all skill levels! This project is specifically designed to be beginner-friendly.

Check out our [CONTRIBUTING.md](docs/CONTRIBUTING.md) for:
- Development setup guide
- Code style guidelines
- Git workflow

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for college students learning web development
- Inspired by VS Code Live Share and collaborative coding tools
- Uses open-source technologies

## 📧 Contact

- Create an issue for bug reports or feature requests
- Check existing issues before creating new ones

---

**Made with ❤️ for the open-source community**
