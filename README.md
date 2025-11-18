# packageTracker
a simple shipping package tracker

## Setup

### Prerequisites
- Docker
- Docker Compose

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/xhiena/packageTracker.git
   cd packageTracker
   ```

2. Create a `.env` file from the example template:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your configuration:
   - Set secure passwords for `POSTGRES_PASSWORD`
   - Configure SMTP settings for email functionality
   - Update `JWT_SECRET` with a secure random string

4. Start the services using Docker Compose:
   ```bash
   docker compose up -d
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Services

- **db**: PostgreSQL database (port 5432)
- **backend**: FastAPI backend server (port 8000)
- **frontend**: React frontend application (port 3000)

### Development

To stop the services:
```bash
docker compose down
```

To rebuild the services after changes:
```bash
docker compose up -d --build
```

To view logs:
```bash
docker compose logs -f
```
