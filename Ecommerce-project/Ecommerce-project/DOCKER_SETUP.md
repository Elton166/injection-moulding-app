# Docker Setup Guide

This guide explains how to run the eCommerce application using Docker containers.

## Prerequisites

- Docker Desktop installed and running
- Docker Hub account (for pulling images)

## Architecture

The application uses two containers:
- **ecommerce_web**: Django application (Python 3.13)
- **ecommerce_db**: MariaDB 12.0.2 database

## Quick Start

### 1. Build the containers

```bash
docker-compose build
```

### 2. Start the containers

```bash
docker-compose up
```

Or run in detached mode (background):

```bash
docker-compose up -d
```

### 3. Access the application

Open your browser and navigate to:
```
http://localhost:8000
```

## Container Management

### View running containers

```bash
docker ps
```

### View logs

```bash
# All logs
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs db

# Follow logs (real-time)
docker-compose logs -f web
```

### Stop containers

```bash
docker-compose down
```

### Rebuild after code changes

```bash
docker-compose down
docker-compose build
docker-compose up
```

## Database Access

The MariaDB database is accessible on:
- **Host**: localhost
- **Port**: 3306
- **Database**: ecommerce_db
- **User**: ecommerce_user
- **Password**: Matthew22

Connect using any MySQL client:

```bash
mysql -h localhost -P 3306 -u ecommerce_user -p ecommerce_db
```

## Environment Variables

The following environment variables are configured in `docker-compose.yml`:

### Web Container
- `DEBUG=True`
- `DB_HOST=db`
- `DB_NAME=ecommerce_db`
- `DB_USER=ecommerce_user`
- `DB_PASSWORD=Matthew22`

### Database Container
- `MYSQL_ROOT_PASSWORD=Matthew22`
- `MYSQL_DATABASE=ecommerce_db`
- `MYSQL_USER=ecommerce_user`
- `MYSQL_PASSWORD=Matthew22`

## Volumes

The setup uses three volumes:
- `mariadb_data`: Persists database data
- `static_volume`: Stores static files
- `media_volume`: Stores uploaded images

## Troubleshooting

### Container won't start

Check logs:
```bash
docker-compose logs web
```

### Database connection errors

Ensure the database container is running:
```bash
docker ps
```

The entrypoint script waits for the database to be ready before starting Django.

### Port already in use

If port 8000 or 3306 is already in use, modify the ports in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Change host port to 8001
```

### Reset everything

To completely reset (WARNING: deletes all data):

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## Development Workflow

1. Make code changes in your editor
2. Changes are automatically reflected (volume mount)
3. For dependency changes, rebuild:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up
   ```

## Production Considerations

For production deployment:

1. Change `DEBUG=False` in environment variables
2. Use a production WSGI server (Gunicorn)
3. Set up proper secrets management
4. Use environment-specific docker-compose files
5. Configure proper logging
6. Set up SSL/TLS certificates
7. Use a reverse proxy (Nginx)

## Files

- `Dockerfile`: Defines the web container
- `docker-compose.yml`: Orchestrates both containers
- `entrypoint.sh`: Startup script that waits for database
- `.dockerignore`: Excludes files from Docker build
