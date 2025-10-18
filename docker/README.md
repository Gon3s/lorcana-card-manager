# 🐳 Docker Setup - Lorcana Card Manager

## 📋 Prerequisites

### Install Docker on WSL

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Logout and login again, then verify
docker --version
docker compose version
```

## 🚀 Quick Start

### 1. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Groq API key
nano .env
```

### 2. Build and Run

```bash
# Build and start all services
docker compose up --build

# Or run in detached mode (background)
docker compose up --build -d
```

### 3. Access

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🛠️ Docker Commands

### Basic Operations

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Stop services
docker compose down

# Rebuild images
docker compose build

# View logs
docker compose logs

# Follow logs
docker compose logs -f

# View logs for specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### Maintenance

```bash
# Restart a service
docker compose restart backend

# Stop and remove all containers, networks, volumes
docker compose down -v

# Execute command in running container
docker compose exec backend bash
docker compose exec backend python seed.py

# Check service status
docker compose ps
```

### Database Operations

```bash
# Initialize database (migrations + seed)
docker compose exec backend ./init_db.sh

# Run migrations only
docker compose exec backend alembic upgrade head

# Create a migration
docker compose exec backend alembic revision -m "description"

# Seed database
docker compose exec backend python seed.py --clear

# Access SQLite database
docker compose exec backend sqlite3 /app/data/lorcana_cards.db
```

## 📁 Volume Structure

```
backend/
├── data/               # SQLite database (Docker volume)
│   └── lorcana_cards.db
├── uploads/            # Uploaded card images (Docker volume)
│   └── YYYY-MM-DD/
│       └── *.jpg
```

These folders are:
- Created automatically in backend/ by Docker volumes
- Persistent across container restarts
- Ignored by Git (see `.gitignore`)

## 🔧 Troubleshooting

### Port already in use

```bash
# Change ports in .env
BACKEND_PORT=8001
FRONTEND_PORT=4201
```

### Permission denied

```bash
# Ensure user is in docker group
sudo usermod -aG docker $USER

# Logout and login again
```

### Database locked

```bash
# Stop all containers
docker compose down

# Remove volumes
docker compose down -v

# Rebuild
docker compose up --build
```

### View container logs

```bash
# All services
docker compose logs

# Specific service
docker compose logs backend
docker compose logs frontend
```

## 🔄 Development Workflow

### Hot Reload

Both backend and frontend support hot reload:

- **Backend**: Code changes are auto-detected (uvicorn --reload)
- **Frontend**: Development server watches for changes

### Debugging

```bash
# Access backend shell
docker compose exec backend bash

# Access Python REPL with app context
docker compose exec backend python

# Check backend health
curl http://localhost:8000/health
```

## 📦 Production Build

For production deployment:

1. Remove `--reload` from backend CMD
2. Use production Angular build
3. Configure proper secrets in `.env`
4. Use a reverse proxy (nginx) in front

## 🌐 Network

Services communicate via `lorcana-network`:
- Backend: accessible at `http://backend:8000` within network
- Frontend proxies API requests to backend

## ⚠️ Important Notes

- **Never commit** `.env` file
- **Backup** `data/` folder regularly
- **Monitor** `uploads/` folder size
- **Update** dependencies periodically

## 📚 Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI in Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Angular in Docker](https://angular.io/guide/deployment)
