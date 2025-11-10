================================================================================
                    ⚠️  IMPORTANT - READ THIS FIRST  ⚠️
================================================================================

FOR REVIEWERS: HOW TO RUN THIS APPLICATION
===========================================

This Django application uses Docker Compose to run TWO containers together:
1. Web container (Django application)
2. Database container (MariaDB)

================================================================================

✅ CORRECT WAY TO RUN:
======================

Step 1: Clone the repository
Step 2: Navigate to project directory
Step 3: Run this command:

    docker-compose up --build

Step 4: Open browser to http://localhost:8000

That's it! Docker Compose will:
- Build the web container
- Pull the MariaDB container
- Create a network for them to communicate
- Wait for database to be ready
- Run migrations automatically
- Start the application

================================================================================

❌ INCORRECT WAY (Will Fail):
=============================

Do NOT try to run the Dockerfile alone:

    docker build -t ecommerce-web .
    docker run -p 8000:8000 ecommerce-web

This will produce the error:
"nc: getaddrinfo for host 'db' port 3306: Name or service not known"

Why? Because the web container expects a database container named 'db'
to exist on the same network. Without Docker Compose, there's no database.

================================================================================

📁 KEY FILES:
=============

- docker-compose.yml  ← This orchestrates both containers (USE THIS!)
- Dockerfile          ← Defines the web container (used by docker-compose)
- entrypoint.sh       ← Waits for database before starting Django
- README.md           ← Full documentation
- DOCKER_INSTRUCTIONS.md ← Detailed Docker setup guide

================================================================================

🧪 VERIFY IT'S WORKING:
=======================

After running docker-compose up, check:

1. Both containers are running:
   docker ps

   You should see:
   - ecommerce_web (port 8000)
   - ecommerce_db (port 3306)

2. Application is accessible:
   Open http://localhost:8000 in browser

3. Database connection works:
   docker-compose exec web python manage.py dbshell

================================================================================

🛑 STOP THE APPLICATION:
========================

Press Ctrl+C in the terminal, or run:

    docker-compose down

================================================================================

📚 MORE INFORMATION:
===================

- README.md - Complete project documentation
- DOCKER_INSTRUCTIONS.md - Detailed Docker setup guide
- docker-compose.yml - Container orchestration configuration

================================================================================

✅ QUICK START SUMMARY:
=======================

1. docker-compose up --build
2. Open http://localhost:8000
3. Done!

================================================================================

This is a multi-container application. Docker Compose is REQUIRED.

================================================================================
