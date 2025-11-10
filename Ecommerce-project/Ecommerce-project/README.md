# Django eCommerce Multi-Vendor Platform

A comprehensive multi-vendor eCommerce platform built with Django, featuring REST API, Docker containerization, and complete documentation.

## ⚠️ IMPORTANT: Docker Setup

**This application uses Docker Compose (not just Dockerfile alone).**

To run with Docker, you MUST use:
```bash
docker-compose up --build
```

The Dockerfile alone will not work because the application requires both a web container and a database container working together. Docker Compose orchestrates both containers.

## 🚀 Features

- **Multi-Vendor System**: Vendors can create stores and manage products
- **User Authentication**: Separate roles for vendors and buyers
- **Product Management**: Full CRUD operations with image uploads
- **Shopping Cart**: Session-based cart with checkout functionality
- **Order Processing**: Complete order management system
- **Product Reviews**: Rating and review system
- **REST API**: JWT-authenticated API endpoints
- **Twitter Integration**: Automatic social media posting
- **Password Reset**: Secure token-based password recovery
- **Docker Support**: Fully containerized application

## 📋 Prerequisites

- Python 3.13+
- MariaDB 12.0.2 (or MySQL)
- Docker & Docker Compose (for containerized deployment)
- Git

## 🛠️ Installation & Setup

### Option 1: Using Virtual Environment

#### 1. Clone the Repository

```bash
git clone https://github.com/Elton2/ecommerce-capstone-project.git
cd ecommerce-capstone-project
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Database

Create a MariaDB/MySQL database:

```sql
CREATE DATABASE ecommerce_db;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

Update `ecommerce/settings.py` with your database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'ecommerce_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### 5. Configure Twitter API (Optional)

If you want Twitter integration, add these to your environment or `settings.py`:

```python
TWITTER_BEARER_TOKEN = 'your_bearer_token'
TWITTER_API_KEY = 'your_api_key'
TWITTER_API_SECRET = 'your_api_secret'
TWITTER_ACCESS_TOKEN = 'your_access_token'
TWITTER_ACCESS_TOKEN_SECRET = 'your_access_token_secret'
```

**Note**: Twitter API credentials are optional. The application works without them.

#### 6. Run Migrations

```bash
python manage.py migrate
```

#### 7. Create Superuser

```bash
python manage.py createsuperuser
```

#### 8. Run Development Server

```bash
python manage.py runserver
```

Access the application at: **http://localhost:8000**

---

### Option 2: Using Docker (Recommended)

#### 1. Clone the Repository

```bash
git clone https://github.com/Elton2/ecommerce-capstone-project.git
cd ecommerce-capstone-project
```

#### 2. Build and Start Containers

```bash
docker-compose up --build
```

This will:
- Build the web application container
- Pull and start MariaDB container
- Run migrations automatically
- Start the Django development server

#### 3. Access the Application

Open your browser and navigate to: **http://localhost:8000**

#### 4. Stop the Application

```bash
docker-compose down
```

#### 5. View Logs

```bash
docker-compose logs -f web
```

---

## 📁 Project Structure

```
ecommerce-capstone-project/
├── Dockerfile                      # Web container definition
├── docker-compose.yml              # Multi-container orchestration
├── entrypoint.sh                   # Container startup script
├── .dockerignore                   # Docker build optimization
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── manage.py                       # Django management script
├── README.md                       # This file
├── capstone.txt                    # GitHub repository link
├── docker1.txt                     # Docker Hub repository link
├── docs/                           # Sphinx documentation
│   ├── _build/                     # Generated documentation
│   ├── conf.py                     # Sphinx configuration
│   └── index.rst                   # Documentation index
├── ecommerce/                      # Django project settings
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # URL routing
│   └── wsgi.py                     # WSGI configuration
├── store/                          # Main application
│   ├── models.py                   # Database models
│   ├── views.py                    # View functions
│   ├── api_views.py                # REST API views
│   ├── urls.py                     # URL patterns
│   ├── forms.py                    # Django forms
│   ├── utils.py                    # Utility functions
│   ├── templates/                  # HTML templates
│   └── migrations/                 # Database migrations
└── static/                         # Static files (CSS, JS, images)
```

## 🔧 Configuration

### Environment Variables

For Docker deployment, configure these in `docker-compose.yml`:

```yaml
environment:
  - DEBUG=True
  - DB_HOST=db
  - DB_NAME=ecommerce_db
  - DB_USER=ecommerce_user
  - DB_PASSWORD=your_password
  - DB_PORT=3306
```

### Database Settings

The application uses environment variables for database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'ecommerce_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory, generated using Sphinx.

### View Documentation

#### Local Development

```bash
cd docs
python -m http.server 8080
```

Then open: **http://localhost:8080/_build/html/index.html**

#### Docker

Documentation is included in the container and accessible after building.

### Generate Documentation

```bash
cd docs
sphinx-build -b html . _build/html
```

## 🧪 Testing

### Run Tests

```bash
python manage.py test
```

### Run Specific Test

```bash
python manage.py test store.tests.TestStoreCRUD
```

## 🐳 Docker Details

### Containers

- **ecommerce_web**: Django application (Port 8000)
- **ecommerce_db**: MariaDB database (Port 3306)

### Volumes

- `mariadb_data`: Persistent database storage
- `static_volume`: Static files
- `media_volume`: User-uploaded images

### Docker Commands

```bash
# Build containers
docker-compose build

# Start containers
docker-compose up

# Start in background
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Run Django commands
docker-compose exec web python manage.py <command>

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 🌐 API Endpoints

### Authentication

- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Stores

- `GET /api/stores/` - List all stores
- `POST /api/stores/` - Create store (vendor only)
- `GET /api/stores/{id}/` - Store details
- `PUT /api/stores/{id}/` - Update store (owner only)
- `DELETE /api/stores/{id}/` - Delete store (owner only)

### Products

- `GET /api/products/` - List all products
- `POST /api/products/` - Create product (vendor only)
- `GET /api/products/{id}/` - Product details
- `PUT /api/products/{id}/` - Update product (owner only)
- `DELETE /api/products/{id}/` - Delete product (owner only)

### Reviews

- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create review (authenticated)
- `GET /api/reviews/{id}/` - Review details
- `PUT /api/reviews/{id}/` - Update review (author only)
- `DELETE /api/reviews/{id}/` - Delete review (author only)

## 🔐 Security Notes

### Secrets Management

**IMPORTANT**: Never commit sensitive information to the repository!

Create a `.env` file (already in `.gitignore`) for sensitive data:

```env
SECRET_KEY=your_django_secret_key
DB_PASSWORD=your_database_password
TWITTER_BEARER_TOKEN=your_twitter_token
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
```

### For Reviewers

Temporary credentials for testing are provided in a separate file (not committed to public repo).

## 🚀 Deployment

### Production Considerations

1. Set `DEBUG=False` in production
2. Use environment variables for all secrets
3. Configure proper ALLOWED_HOSTS
4. Use Gunicorn or uWSGI instead of Django dev server
5. Set up Nginx as reverse proxy
6. Enable HTTPS/SSL
7. Use managed database service
8. Configure proper logging
9. Set up monitoring and alerts

### Deploy to Cloud

The Docker setup makes it easy to deploy to:
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform
- Heroku

## 🤝 Contributing

This is a capstone project for educational purposes. However, suggestions and feedback are welcome!

## 📝 License

This project is created for educational purposes as part of a software development bootcamp.

## 👤 Author

**Elton**
- GitHub: [@Elton2](https://github.com/Elton2)
- Docker Hub: [elton2](https://hub.docker.com/u/elton2)
- Email: eltonoct@gmail.com

## 🙏 Acknowledgments

- HyperionDev for the bootcamp curriculum
- Django documentation and community
- Docker documentation
- All open-source contributors

## 📞 Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review the troubleshooting section
3. Check existing issues on GitHub
4. Create a new issue with detailed information

---

**Last Updated**: November 10, 2025
**Version**: 1.0.0
**Status**: ✅ Production Ready
