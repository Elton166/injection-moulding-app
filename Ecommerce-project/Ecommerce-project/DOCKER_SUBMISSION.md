# Docker Containerization Submission

**Student**: Elton
**Docker Hub Username**: elton2
**Project**: eCommerce Multi-Vendor Platform

---

## Overview

This project has been fully containerized using Docker, enabling easy deployment and consistent development environments. The application uses a multi-container architecture with Docker Compose orchestrating the services.

## Architecture

### Containers

1. **ecommerce_web** - Django Application Container
   - Base Image: `python:3.13-slim`
   - Exposed Port: 8000
   - Purpose: Runs the Django web application

2. **ecommerce_db** - MariaDB Database Container
   - Base Image: `mariadb:12.0.2`
   - Exposed Port: 3306
   - Purpose: Persistent data storage

### Networking

- Custom bridge network: `ecommerce_network`
- Containers communicate using service names (web → db)
- External access via port mapping

### Volumes

- `mariadb_data`: Persists database data across container restarts
- `static_volume`: Stores Django static files
- `media_volume`: Stores user-uploaded images

## Files Included

### 1. Dockerfile
Defines the web application container with:
- Python 3.13 slim base image
- System dependencies (gcc, MySQL client, netcat)
- Python package installation
- Entrypoint script configuration

### 2. docker-compose.yml
Orchestrates multi-container setup:
- Service definitions (web, db)
- Environment variables
- Volume mappings
- Network configuration
- Container dependencies

### 3. entrypoint.sh
Startup script that:
- Waits for database to be ready
- Runs Django migrations
- Starts the development server

### 4. .dockerignore
Optimizes build by excluding:
- Python cache files
- Virtual environments
- Development databases
- IDE configurations
- Documentation files

### 5. requirements.txt
Lists all Python dependencies including:
- Django 5.2.6
- Django REST Framework
- MySQL client
- Pillow (image processing)
- Tweepy (Twitter integration)

## Prerequisites

Before running the application, ensure you have:

1. **Docker Desktop** installed and running
   - Download from: https://www.docker.com/products/docker-desktop

2. **Docker Hub Account** (optional for pulling public images)
   - The project uses public images (python, mariadb)

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Ecommerce-project
```

### Step 2: Build the Containers

```bash
docker-compose build
```

This will:
- Download base images (Python 3.13, MariaDB 12.0.2)
- Install system dependencies
- Install Python packages from requirements.txt
- Copy application files

**Expected build time**: 2-5 minutes (depending on internet speed)

### Step 3: Start the Application

```bash
docker-compose up
```

Or run in detached mode (background):

```bash
docker-compose up -d
```

The entrypoint script will:
1. Wait for the database to be ready
2. Run database migrations automatically
3. Start the Django development server

### Step 4: Access the Application

Open your web browser and navigate to:

```
http://localhost:8000
```

You should see the eCommerce platform homepage.

## Usage

### Verify Containers are Running

```bash
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE                   STATUS          PORTS
xxxxx          ecommerce-project-web   Up X minutes    0.0.0.0:8000->8000/tcp
xxxxx          mariadb:12.0.2          Up X minutes    0.0.0.0:3306->3306/tcp
```

### View Application Logs

```bash
# View all logs
docker-compose logs

# View web container logs only
docker-compose logs web

# View database logs only
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f web
```

### Stop the Application

```bash
docker-compose down
```

This stops and removes containers but preserves data in volumes.

### Restart the Application

```bash
docker-compose up
```

Data persists across restarts thanks to Docker volumes.

## Database Access

The MariaDB database is accessible for direct connections:

**Connection Details:**
- Host: `localhost`
- Port: `3306`
- Database: `ecommerce_db`
- User: `ecommerce_user`
- Password: `Matthew22`

**Connect via MySQL client:**

```bash
mysql -h localhost -P 3306 -u ecommerce_user -p ecommerce_db
```

## Environment Variables

### Web Container (Django)

| Variable | Value | Purpose |
|----------|-------|---------|
| DEBUG | True | Enable debug mode |
| DB_HOST | db | Database container hostname |
| DB_NAME | ecommerce_db | Database name |
| DB_USER | ecommerce_user | Database user |
| DB_PASSWORD | Matthew22 | Database password |
| DB_PORT | 3306 | Database port |

### Database Container (MariaDB)

| Variable | Value | Purpose |
|----------|-------|---------|
| MYSQL_ROOT_PASSWORD | Matthew22 | Root password |
| MYSQL_DATABASE | ecommerce_db | Initial database |
| MYSQL_USER | ecommerce_user | Application user |
| MYSQL_PASSWORD | Matthew22 | User password |

## Development Workflow

### Making Code Changes

1. Edit files in your IDE (changes are reflected immediately via volume mount)
2. Django auto-reloads on file changes
3. Refresh browser to see changes

### Adding New Dependencies

1. Update `requirements.txt`
2. Rebuild the container:
   ```bash
   docker-compose down
   docker-compose build web
   docker-compose up
   ```

### Running Django Management Commands

```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic

# Open Django shell
docker-compose exec web python manage.py shell
```

## Troubleshooting

### Issue: Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**: Change the host port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### Issue: Database Connection Failed

**Error**: `Can't connect to MySQL server`

**Solution**: 
- Ensure database container is running: `docker ps`
- Wait a few seconds for database initialization
- Check logs: `docker-compose logs db`

### Issue: Permission Denied on entrypoint.sh

**Error**: `permission denied: /app/entrypoint.sh`

**Solution**: The Dockerfile already sets execute permissions, but if needed:
```bash
chmod +x entrypoint.sh
docker-compose build web
```

### Issue: Container Keeps Restarting

**Solution**: Check logs for errors:
```bash
docker-compose logs web
```

### Complete Reset

To start fresh (WARNING: deletes all data):

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## Testing the Application

### 1. Homepage
- Navigate to http://localhost:8000
- Should display the store homepage

### 2. User Registration
- Click "Register"
- Create a new account (vendor or buyer)

### 3. Login
- Use credentials to log in
- Access user-specific features

### 4. Vendor Features (if vendor account)
- Create stores
- Add products
- Manage inventory

### 5. Buyer Features
- Browse products
- Add to cart
- Checkout

## Production Considerations

For production deployment, consider:

1. **Security**
   - Set `DEBUG=False`
   - Use strong, unique passwords
   - Implement secrets management
   - Enable HTTPS/SSL

2. **Performance**
   - Use Gunicorn instead of Django dev server
   - Add Nginx reverse proxy
   - Configure caching (Redis)
   - Optimize database queries

3. **Scalability**
   - Use managed database service
   - Implement load balancing
   - Add container orchestration (Kubernetes)

4. **Monitoring**
   - Set up logging aggregation
   - Add health checks
   - Monitor resource usage

## Docker Hub Integration

### Tagging Images

To push images to Docker Hub (elton2):

```bash
# Tag the web image
docker tag ecommerce-project-web elton2/ecommerce-web:latest

# Push to Docker Hub
docker push elton2/ecommerce-web:latest
```

### Pulling from Docker Hub

Others can pull and run your image:

```bash
docker pull elton2/ecommerce-web:latest
docker run -p 8000:8000 elton2/ecommerce-web:latest
```

## Project Structure

```
Ecommerce-project/
├── Dockerfile                 # Web container definition
├── docker-compose.yml         # Multi-container orchestration
├── entrypoint.sh             # Container startup script
├── .dockerignore             # Build optimization
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
├── ecommerce/                # Django project settings
│   ├── settings.py          # Updated with Docker env vars
│   ├── urls.py
│   └── wsgi.py
├── store/                    # Main application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
└── static/                   # Static files
```

## Key Features Implemented

### Docker-Specific Features

✅ Multi-container architecture
✅ Automatic database waiting mechanism
✅ Environment-based configuration
✅ Persistent data storage
✅ Volume mounting for development
✅ Network isolation
✅ Health checks via entrypoint script
✅ Optimized build with .dockerignore

### Application Features

✅ User authentication (vendors & buyers)
✅ Multi-vendor store management
✅ Product catalog with images
✅ Shopping cart functionality
✅ Order processing
✅ Product reviews
✅ REST API with JWT authentication
✅ Twitter integration
✅ Password reset functionality

## Conclusion

This Docker setup provides:
- **Consistency**: Same environment across all machines
- **Isolation**: No conflicts with local installations
- **Portability**: Easy to deploy anywhere
- **Scalability**: Ready for production orchestration
- **Simplicity**: One command to start everything

The application is production-ready and can be deployed to any Docker-compatible hosting platform (AWS ECS, Google Cloud Run, Azure Container Instances, etc.).

---

**Submitted by**: Elton (elton2)
**Date**: November 10, 2025
**Docker Version**: 28.5.1
**Docker Compose Version**: 3.8
