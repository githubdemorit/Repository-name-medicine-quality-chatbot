# 🚀 Complete Deployment Guide - Medicine Quality Chatbot

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Node.js 16+
- Git
- Virtual Environment tool (venv)

### Step 1: Clone and Navigate to Repository

```bash
git clone https://github.com/githubdemorit/Repository-name-medicine-quality-chatbot.git
cd Repository-name-medicine-quality-chatbot
```

### Step 2: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Important variables to update:**
- `OPENAI_API_KEY`: Get from https://platform.openai.com/api-keys
- `JWT_SECRET`: Generate a strong secret key
- `DB_PASSWORD`: Change from default
- `DATABASE_URL`: Update if using remote DB

### Step 3: Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Set Up PostgreSQL Database

```bash
# Option A: Using Docker (Recommended)
docker run --name medicine_db \
  -e POSTGRES_USER=medicinebot \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=medicine_quality_db \
  -p 5432:5432 \
  -d postgres:15-alpine

# Option B: Using local PostgreSQL
# Create database
createdb -U postgres medicine_quality_db

# Create user
psql -U postgres -c "CREATE USER medicinebot WITH PASSWORD 'your_password';"
psql -U postgres -c "ALTER ROLE medicinebot WITH CREATEDB;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE medicine_quality_db TO medicinebot;"
```

### Step 6: Initialize Database Schema

```bash
# Run database migrations (if using Alembic)
alembic upgrade head

# Or create tables directly (placeholder)
python -c "from main import app; print('App loaded successfully')"
```

### Step 7: Run Development Server

```bash
# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, test the API
curl http://localhost:8000/health
```

Access the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Docker Deployment

### Single Command Deployment

```bash
# Ensure .env file is configured
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Verify Services

```bash
# Check running containers
docker-compose ps

# Test backend health
curl http://localhost:8000/health

# Access API docs
# http://localhost:8000/docs
```

### Docker Commands Reference

```bash
# Build images
docker-compose build

# View logs for specific service
docker-compose logs backend

# Execute command in container
docker-compose exec backend bash

# Rebuild and restart
docker-compose down && docker-compose up -d --build

# Stop all services
docker-compose down

# Remove volumes (WARNING: Deletes data)
docker-compose down -v
```

---

## Production Deployment

### Option 1: Deploy on AWS EC2

#### Step 1: Launch EC2 Instance

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker ubuntu
```

#### Step 2: Clone Repository

```bash
cd /home/ubuntu
git clone https://github.com/githubdemorit/Repository-name-medicine-quality-chatbot.git
cd Repository-name-medicine-quality-chatbot
```

#### Step 3: Configure for Production

```bash
# Copy and edit environment for production
cp .env.example .env
sudo nano .env
```

**Update these for production:**
```
DEBUG=False
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com
OPENAI_API_KEY=your_actual_key
JWT_SECRET=generate_strong_secret_key
DB_PASSWORD=strong_database_password
```

#### Step 4: Deploy with Docker

```bash
# Start services
sudo docker-compose up -d

# Verify
sudo docker-compose ps
```

---

### Option 2: Deploy on Heroku

#### Step 1: Install Heroku CLI

```bash
curl https://cli.heroku.com/install.sh | sh
heroku login
```

#### Step 2: Create Heroku App

```bash
# Create app
heroku create your-medicine-chatbot

# Add PostgreSQL add-on
heroku addons:create heroku-postgresql:mini -a your-medicine-chatbot

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key -a your-medicine-chatbot
heroku config:set JWT_SECRET=your_secret -a your-medicine-chatbot
heroku config:set ENVIRONMENT=production -a your-medicine-chatbot
```

#### Step 3: Deploy

```bash
# Deploy from Git
git push heroku main

# View logs
heroku logs --tail -a your-medicine-chatbot

# Scale dynos if needed
heroku ps:scale web=1 -a your-medicine-chatbot
```

---

### Option 3: Deploy on Google Cloud Run

#### Step 1: Setup GCP Project

```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# Initialize
gcloud init
gcloud auth login
```

#### Step 2: Create Container Image

```bash
# Build image
docker build -t gcr.io/your-project-id/medicine-chatbot:latest .

# Push to Container Registry
docker push gcr.io/your-project-id/medicine-chatbot:latest
```

#### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy medicine-chatbot \
  --image gcr.io/your-project-id/medicine-chatbot:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production,OPENAI_API_KEY=your_key
```

---

## API Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Is this medicine genuine?",
    "medicine_name": "Aspirin",
    "batch_number": "ABC123"
  }'
```

### Get Medicine Info

```bash
curl http://localhost:8000/api/v1/medicine/Aspirin
```

### Verify Batch

```bash
curl -X POST http://localhost:8000/api/v1/verify-batch \
  -H "Content-Type: application/json" \
  -d '{
    "batch_number": "ABC123",
    "qr_code": "data:image/png;base64,..."
  }'
```

---

## Monitoring & Logs

### Docker Logs

```bash
# View backend logs
docker-compose logs -f backend

# View database logs
docker-compose logs -f db

# View specific lines
docker-compose logs --tail=100 backend
```

### Application Monitoring

```bash
# Check container stats
docker stats

# View resource usage
docker-compose stats
```

---

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Test connection
psql -U medicinebot -d medicine_quality_db -h localhost

# Restart database
docker-compose restart db
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port in docker-compose.yml
# Change "8000:8000" to "8001:8000"
```

### Module Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Docker Build Failures

```bash
# Clean build
docker-compose build --no-cache

# Check logs
docker-compose build --no-cache backend

# Rebuild from scratch
docker system prune -a
docker-compose up -d --build
```

---

## Security Best Practices

1. **Environment Variables**: Never commit `.env` to Git
2. **Secrets Management**: Use proper secret management (AWS Secrets Manager, Heroku Config Vars)
3. **Database**: Always use strong passwords
4. **HTTPS**: Enable SSL/TLS in production
5. **API Keys**: Rotate keys regularly
6. **Dependencies**: Keep packages updated

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update packages
pip install --upgrade -r requirements.txt
```

---

## Performance Optimization

### Caching

```python
# Configure Redis in .env
REDIS_URL=redis://localhost:6379/0

# Use in code
from redis import Redis
redis_client = Redis.from_url(os.getenv("REDIS_URL"))
```

### Database Optimization

```bash
# Create indexes
psql -U medicinebot -d medicine_quality_db -c \
  "CREATE INDEX idx_batch_number ON medicines(batch_number);"
```

### Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py and run
locust -f locustfile.py --host=http://localhost:8000
```

---

## Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

## Support

For issues and questions:
1. Check logs: `docker-compose logs`
2. Review documentation in `/docs`
3. Create GitHub issue with detailed error information
4. Include: logs, environment info, reproduction steps
