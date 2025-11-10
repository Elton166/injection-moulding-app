# Project Structure

## 📁 Proper Django Project Organization

This document explains the correct structure for this Django eCommerce project.

## Root Directory Structure

```
Ecommerce-project/
├── manage.py                 # Django management script (KEEP)
├── requirements.txt          # Python dependencies (KEEP)
├── .gitignore               # Git ignore file (KEEP)
├── README.md                # Main documentation (KEEP)
├── db.sqlite3               # SQLite database (development only)
│
├── ecommerce/               # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Main configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── store/                   # Main application
│   ├── __init__.py
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── api_views.py         # API endpoints
│   ├── serializers.py       # API serializers
│   ├── permissions.py       # Custom permissions
│   ├── utils.py             # Utility functions
│   ├── templates/           # HTML templates
│   │   ├── store/
│   │   └── registration/
│   └── migrations/          # Database migrations
│
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── docs/                    # Documentation
│   ├── API_ENDPOINTS.md
│   ├── API_PLANNING.md
│   ├── TWITTER_SETUP_GUIDE.md
│   ├── PROJECT_PLANNING.md
│   ├── TESTING.md
│   └── tests/               # Test scripts
│       ├── test_api.py
│       ├── test_mariadb_setup.py
│       ├── check_db_status.py
│       └── final_mariadb_test.py
│
└── env/                     # Virtual environment (NEVER COMMIT!)
    └── (excluded via .gitignore)
```

## ⚠️ Files That Should NOT Be in Root

The following files should be moved or removed:

### Test Files (Move to `docs/tests/`)
- `test_api.py` → `docs/tests/test_api.py`
- `test_mariadb_setup.py` → `docs/tests/test_mariadb_setup.py`
- `test_twitter_free_tier.py` → `docs/tests/test_twitter_free_tier.py`
- `final_mariadb_test.py` → `docs/tests/final_mariadb_test.py`
- `check_db_status.py` → `docs/tests/check_db_status.py`
- `test_admin_login.py` → `docs/tests/test_admin_login.py`
- `test_user_registration.py` → `docs/tests/test_user_registration.py`
- `quick_api_test.py` → `docs/tests/quick_api_test.py`
- `verify_web_interface.py` → `docs/tests/verify_web_interface.py`

### Documentation Files (Move to `docs/`)
- `API_PLANNING.md` → `docs/API_PLANNING.md`
- `API_SEQUENCE_DIAGRAMS.md` → `docs/API_SEQUENCE_DIAGRAMS.md`
- `API_IMPLEMENTATION_SUMMARY.md` → `docs/API_IMPLEMENTATION_SUMMARY.md`
- `TWITTER_SETUP_GUIDE.md` → `docs/TWITTER_SETUP_GUIDE.md`
- `TWITTER_FREE_TIER_UPDATE.md` → `docs/TWITTER_FREE_TIER_UPDATE.md`
- `PROJECT_PLANNING.md` → `docs/PROJECT_PLANNING.md`
- `IMPLEMENTATION_SUMMARY.md` → `docs/IMPLEMENTATION_SUMMARY.md`
- `CURRENCY_UPDATE_SUMMARY.md` → `docs/CURRENCY_UPDATE_SUMMARY.md`
- `MARIADB_SUBMISSION_REPORT.md` → `docs/MARIADB_SUBMISSION_REPORT.md`
- `FIXES_APPLIED.md` → `docs/FIXES_APPLIED.md`

### Setup Scripts (Move to `scripts/`)
- `setup_mariadb.py` → `scripts/setup_mariadb.py`
- `manual_test_guide.py` → `scripts/manual_test_guide.py`

### Temporary/Backup Files (DELETE)
- `sqlite_backup.json` (backup file, regenerate when needed)
- `test_logout.html` (test file, not needed)

### Docker Files (Keep in root OR move to `docker/`)
If you have Docker files, they can stay in root:
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

Or move to a `docker/` directory for better organization.

## 🚫 NEVER Commit These

Add to `.gitignore`:

```gitignore
# Virtual Environment
env/
venv/
ENV/
.venv/

# Database
*.sqlite3
db.sqlite3
*.db

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Backup files
*.bak
*.backup
sqlite_backup.json

# Environment variables
.env
.env.local

# Media files (user uploads)
/media/

# Static files (collected)
/staticfiles/
/static_root/
```

## ✅ Proper Root Directory

After cleanup, your root should only contain:

```
Ecommerce-project/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── db.sqlite3 (development only)
├── ecommerce/
├── store/
├── static/
├── docs/
├── scripts/ (optional)
└── docker/ (optional)
```

## 🔧 How to Clean Up

### 1. Create directories
```bash
mkdir -p docs/tests
mkdir -p scripts
```

### 2. Move test files
```bash
# Windows
move test_*.py docs\tests\
move check_db_status.py docs\tests\
move final_mariadb_test.py docs\tests\
move quick_api_test.py docs\tests\
move verify_web_interface.py docs\tests\

# Linux/Mac
mv test_*.py docs/tests/
mv check_db_status.py docs/tests/
mv final_mariadb_test.py docs/tests/
mv quick_api_test.py docs/tests/
mv verify_web_interface.py docs/tests/
```

### 3. Move documentation
```bash
# Windows
move *_SUMMARY.md docs\
move *_PLANNING.md docs\
move TWITTER_*.md docs\
move API_*.md docs\
move FIXES_APPLIED.md docs\

# Linux/Mac
mv *_SUMMARY.md docs/
mv *_PLANNING.md docs/
mv TWITTER_*.md docs/
mv API_*.md docs/
mv FIXES_APPLIED.md docs/
```

### 4. Move setup scripts
```bash
# Windows
move setup_mariadb.py scripts\
move manual_test_guide.py scripts\

# Linux/Mac
mv setup_mariadb.py scripts/
mv manual_test_guide.py scripts/
```

### 5. Delete temporary files
```bash
# Windows
del sqlite_backup.json
del test_logout.html

# Linux/Mac
rm sqlite_backup.json
rm test_logout.html
```

### 6. Remove virtual environment if committed
```bash
# Windows
rmdir /s /q env

# Linux/Mac
rm -rf env/
```

Then create a fresh virtual environment:
```bash
python -m venv env
```

## 📝 Best Practices

1. **Never commit `env/`** - Always in `.gitignore`
2. **Keep root clean** - Only essential files
3. **Organize by purpose** - Tests in `tests/`, docs in `docs/`
4. **Use meaningful names** - Clear file and folder names
5. **Document structure** - Keep this file updated

## 🎯 Benefits of Clean Structure

- ✅ Easier to navigate
- ✅ Professional appearance
- ✅ Easier to maintain
- ✅ Better collaboration
- ✅ Clearer purpose of each file
- ✅ Follows Django best practices

---

**Remember**: A clean project structure shows professionalism and makes your code easier to understand and maintain!