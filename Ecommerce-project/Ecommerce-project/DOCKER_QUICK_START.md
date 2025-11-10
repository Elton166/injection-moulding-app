# Docker Quick Start Guide

**For Instructors/Reviewers**: Fast setup instructions

---

## TL;DR - Run the Application

```bash
# 1. Build containers
docker-compose build

# 2. Start application
docker-compose up

# 3. Open browser
http://localhost:8000
```

That's it! The application is now running.

---

## What's Running?

Two containers:
- **ecommerce_web** (Django) on port 8000
- **ecommerce_db** (MariaDB) on port 3306

---

## Verify It's Working

### Check containers are running:
```bash
docker ps
```

### Test the application:
```bash
curl http://localhost:8000
```

Should return HTTP 200 with HTML content.

---

## Stop the Application

```bash
docker-compose down
```

---

## View Logs

```bash
docker-compose logs -f web
```

---

## Run Django Commands

```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell
```

---

## Files to Review

1. **Dockerfile** - Web container configuration
2. **docker-compose.yml** - Multi-container setup
3. **entrypoint.sh** - Startup script with DB wait logic
4. **.dockerignore** - Build optimization
5. **ecommerce/settings.py** - Environment variable configuration (lines 82-93)

---

## Key Implementation Details

### Database Connection Handling
The `entrypoint.sh` script waits for MariaDB to be ready before starting Django:
```bash
while ! nc -z db 3306; do
  sleep 1
done
```

### Environment Variables
Django reads database config from environment (see `settings.py`):
```python
'HOST': os.environ.get('DB_HOST', 'localhost')
```

### Automatic Migrations
Migrations run automatically on container startup via `entrypoint.sh`.

---

## Test Scenarios

### 1. Fresh Start
```bash
docker-compose down -v
docker-compose up --build
```

### 2. Access Homepage
Navigate to http://localhost:8000

### 3. Register User
Click "Register" → Create vendor account

### 4. Create Store
Login → Create new store

### 5. Add Product
Add product to your store

---

## Troubleshooting

**Containers won't start?**
```bash
docker-compose logs
```

**Port conflict?**
Change port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"
```

**Need fresh database?**
```bash
docker-compose down -v
docker-compose up
```

---

## Docker Hub Account

**Username**: elton2
**Email**: eltonoct@gmail.com

Images can be pushed to: `elton2/ecommerce-web`

---

## Submission Checklist

✅ Dockerfile created
✅ docker-compose.yml configured
✅ entrypoint.sh with database wait logic
✅ .dockerignore for optimization
✅ Environment variables configured
✅ Multi-container networking working
✅ Persistent volumes configured
✅ Application accessible on localhost:8000
✅ Documentation provided

---

**Ready for Review**: Yes ✅
**Tested**: Yes ✅
**Working**: Yes ✅
