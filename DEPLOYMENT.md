# Deployment Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- (Optional) Gmail account for SMTP password recovery

## Quick Start

### 1. Clone and Configure

```bash
git clone https://github.com/xhiena/packageTracker.git
cd packageTracker
```

### 2. Environment Configuration

Copy the example environment file:
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and update:
```env
# REQUIRED: Change this to a strong random key in production!
SECRET_KEY=your-secret-key-here-change-in-production

# OPTIONAL: For password recovery feature
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
```

### 3. Start the Application

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- FastAPI backend on port 8000
- React frontend on port 3000

### 4. Verify Deployment

Check that all services are running:
```bash
docker-compose ps
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## First-Time Setup

### 1. Register a User

Open http://localhost:3000 and click "Register here". Create your first user account.

### 2. Add a Package

After logging in:
1. Select a carrier (Correos or GLS)
2. Enter a valid tracking number:
   - Correos: `AB123456789ES` (format: 2 letters + 9 digits + 2 letters)
   - GLS: `12345678901` (format: 11 digits)
3. Add an optional description
4. Click "Add Package"

### 3. Track Your Package

Click "Track Package" on any package card to see the tracking history and current status.

## SMTP Setup for Password Recovery

### Using Gmail

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and your device
   - Copy the generated 16-character password
3. Update `backend/.env`:
   ```env
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   SMTP_FROM=your-email@gmail.com
   ```
4. Restart the backend:
   ```bash
   docker-compose restart backend
   ```

### Using Other SMTP Providers

Update the SMTP settings in `backend/.env`:
```env
SMTP_HOST=smtp.yourprovider.com
SMTP_PORT=587
SMTP_USER=your-username
SMTP_PASSWORD=your-password
SMTP_FROM=noreply@yourdomain.com
```

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value (use `openssl rand -hex 32`)
- [ ] Update database credentials in `docker-compose.yml`
- [ ] Configure proper CORS origins in `backend/app/main.py`
- [ ] Set up HTTPS with reverse proxy (nginx/traefik)
- [ ] Enable database backups
- [ ] Set up logging and monitoring
- [ ] Review and update SMTP settings

### Docker Compose Production Configuration

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  db:
    restart: always
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    restart: always
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      SECRET_KEY: ${SECRET_KEY}
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

  frontend:
    restart: always
    environment:
      REACT_APP_API_URL: https://api.yourdomain.com

volumes:
  postgres_data:
```

Deploy with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Reverse Proxy (nginx)

Example nginx configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Scaling

### Horizontal Scaling

The application is stateless and can be scaled horizontally:

```yaml
backend:
  deploy:
    replicas: 4
  command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Database Scaling

For high-traffic scenarios:
1. Enable PostgreSQL connection pooling
2. Add read replicas for read-heavy operations
3. Implement caching layer (Redis)

## Monitoring

### Health Checks

The backend provides a health check endpoint:
```bash
curl http://localhost:8000/health
```

### Logs

View logs for each service:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Metrics

Consider adding:
- Prometheus for metrics collection
- Grafana for visualization
- Sentry for error tracking

## Backup and Recovery

### Database Backup

```bash
# Backup
docker-compose exec db pg_dump -U packagetracker packagetracker > backup.sql

# Restore
docker-compose exec -T db psql -U packagetracker packagetracker < backup.sql
```

### Automated Backups

Add to crontab:
```bash
0 2 * * * cd /path/to/packageTracker && docker-compose exec db pg_dump -U packagetracker packagetracker > backups/backup-$(date +\%Y\%m\%d).sql
```

## Troubleshooting

### Backend won't start

1. Check database connection:
   ```bash
   docker-compose logs db
   ```

2. Verify environment variables:
   ```bash
   docker-compose exec backend env | grep DATABASE_URL
   ```

### Frontend can't connect to backend

1. Check CORS configuration in `backend/app/main.py`
2. Verify `REACT_APP_API_URL` in frontend environment
3. Check network connectivity:
   ```bash
   docker-compose exec frontend ping backend
   ```

### Tests failing

Run tests locally:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest --cov=app
```

## Maintenance

### Update Dependencies

Backend:
```bash
cd backend
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

Frontend:
```bash
cd frontend
npm update
npm audit fix
```

### Database Migrations

When adding new models:
```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
docker-compose exec backend alembic upgrade head
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/xhiena/packageTracker/issues
- Documentation: See README.md and ARCHITECTURE.md
