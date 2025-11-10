# Testing Documentation

This directory contains all testing-related files and documentation.

## Test Files

- `test_api.py` - API endpoint testing
- `test_mariadb_setup.py` - Database setup testing
- `test_twitter_free_tier.py` - Twitter integration testing
- `final_mariadb_test.py` - Comprehensive MariaDB tests
- `check_db_status.py` - Database status checker

## Running Tests

```bash
# Test database connection
python docs/tests/check_db_status.py

# Test MariaDB functionality
python docs/tests/final_mariadb_test.py

# Test API endpoints
python docs/tests/test_api.py

# Test Twitter integration
python docs/tests/test_twitter_free_tier.py
```

## Test Coverage

All major features are covered:
- User authentication
- Store management
- Product management
- API endpoints
- Database operations
- Twitter integration
