# Ghost Labs - Setup Guide

## Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Ghost-Labs.git
cd Ghost-Labs
```

### 2. Start Everything
```bash
docker-compose up -d
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/health

## Development Setup

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:socket_app --reload --port 8000
```

## Docker Commands

```bash
# Build workspace image
docker build -t ghost-labs-workspace:latest -f docker/workspace/Dockerfile docker/workspace

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild backend service
docker-compose up -d --build backend
```

## Troubleshooting

### Port Already in Use
If ports 3000 or 8000 are in use:
1. Stop the conflicting service
2. Or change the port in `docker-compose.yml` and `backend/main.py`

### Docker Permission Denied
On Linux, you may need to add your user to docker group:
```bash
sudo usermod -aG docker $USER
```
Then log out and back in.

## Need Help?

- Open an issue on GitHub
- Check existing documentation
- Look at similar implementations in the codebase

---

**Made with ❤️ for the open-source community**
