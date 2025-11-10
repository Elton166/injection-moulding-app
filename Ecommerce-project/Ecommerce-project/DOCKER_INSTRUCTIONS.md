# Docker Setup Instructions

## ⚠️ IMPORTANT: Use Docker Compose

**This application requires Docker Compose to run properly.**

The Dockerfile alone will NOT work because the application needs:
1. A web container (Django application)
2. A database container (MariaDB)

Docker Compose orchestrates both containers to work together.

---

## 🚀 How to Run with Docker Compose

### Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Elton166/ecommerce-capstone-project.git
cd ecommerce-capstone-project
```

### Step 2: Build and Start with Docker Compose

```bash
docker-compose up --build
```

This single command will:
- Build the web application container
- Pull the MariaDB database container
- Create a network for containers to communicate
- Wait for the database to be ready
- Run database migrations automatically
- Start the Django development server

### Step 3: Access the Application

Open your browser and go to:
```
http://localhost:8000
```

### Step 4: Stop the Application

Press `Ctrl+C` in the terminal, or run:
```bash
docker-compose down
```

---

## 🔧 What Docker Compose Does

The `docker-compose.yml` file defines two services:

### 1. Database Service (db)
- **Image**: mariadb:12.0.2
- **Port**: 3306
- **Database**: ecommerce_db
- **User**: ecommerce_user
- **Password**: Matthew22

### 2. Web Service (web)
- **Built from**: Dockerfile
- **Port**: 8000
- **Depends on**: db service
- **Environment**: Configured to connect to db container

### Network
Both containers are connected via a custom bridge network called `ecommerce_network`, allowing them to communicate using service names (e.g., `db` as hostname).

---

## ❌ Why Dockerfile Alone Doesn't Work

If you try to run just the Docker image:

```bash
docker build -t ecommerce-web .
docker run -p 8000:8000 ecommerce-web
```

You'll get this error:
```
nc: getaddrinfo for host 'db' port 3306: Name or service not known
```

**Why?** The web container expects a database container named `db` to exist on the same network. Without Docker Compose, there's no database container, so the connection fails.

---

## ✅ Correct Way: Use Docker Compose

Always use Docker Compose to run this application:

```bash
# Start everything
docker-compose up

# Or start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

---

## 🧪 Testing the Setup

### Verify Both Containers are Running

```bash
docker ps
```

You should see:
```
CONTAINER ID   IMAGE                   STATUS          PORTS
xxxxx          ecommerce-project-web   Up X minutes    0.0.0.0:8000->8000/tcp
xxxxx          mariadb:12.0.2          Up X minutes    0.0.0.0:3306->3306/tcp
```

### Test the Application

```bash
curl http://localhost:8000
```

Should return HTTP 200 with HTML content.

### Check Database Connection

```bash
docker-compose exec web python manage.py dbshell
```

This should connect to the MariaDB database.

---

## 📝 For Reviewers

**To test this application:**

1. Clone the repository
2. Navigate to project directory
3. Run: `docker-compose up --build`
4. Open: http://localhost:8000

**Do NOT try to run the Dockerfile alone** - it requires Docker Compose to work with the database.

---

## 🔍 Architecture Diagram

```
┌─────────────────────────────────────────┐
│      Docker Compose Network             │
│                                         │
│  ┌──────────────┐    ┌──────────────┐ │
│  │ ecommerce_web│◄───┤ ecommerce_db │ │
│  │  (Django)    │    │  (MariaDB)   │ │
│  │  Port: 8000  │    │  Port: 3306  │ │
│  └──────┬───────┘    └──────────────┘ │
│         │                               │
└─────────┼───────────────────────────────┘
          │
          ▼
    http://localhost:8000
```

---

## 🛠️ Troubleshooting

### Error: "nc: getaddrinfo for host 'db'"

**Cause**: Trying to run Dockerfile alone without Docker Compose

**Solution**: Use `docker-compose up` instead

### Error: "port is already allocated"

**Cause**: Port 8000 or 3306 is already in use

**Solution**: Stop other services or change ports in docker-compose.yml:
```yaml
ports:
  - "8001:8000"  # Use different host port
```

### Error: "Cannot connect to database"

**Cause**: Database container not ready yet

**Solution**: The entrypoint.sh script handles this automatically. Wait a few seconds.

---

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Deploy Django using Docker Compose](https://medium.com/powered-by-django/deploy-django-using-docker-compose-windows-3068f2d981c4)
- [Docker Networking](https://docs.docker.com/network/)

---

## ✅ Summary

**✓ DO**: Use `docker-compose up`  
**✗ DON'T**: Use `docker run` with just the Dockerfile

The application is designed to work with Docker Compose, which manages both the web and database containers together.

---

**Questions?** Check the README.md or create an issue on GitHub.
