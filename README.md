# 📚 LibraryPlatform

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://docker.com)
[![Code Style](https://img.shields.io/badge/Code%20Style-Google%20%7C%20Make%20Python-orange.svg)](https://google.github.io/styleguide/pyguide.html)

A modern, scalable REST API for managing books and authors in a library system. Built with FastAPI, SQLAlchemy, and PostgreSQL, featuring comprehensive authentication, book management, and bulk import capabilities.

## ✨ Features

- 🔐 **JWT Authentication** - Secure token-based authentication with refresh tokens
- 👤 **Author Management** - Complete CRUD operations for authors
- 📖 **Book Management** - Advanced book catalog with filtering and search
- 📥 **Bulk Import** - Import books from CSV and JSON files
- 🐳 **Docker Ready** - Full containerization with Docker Compose
- 🗄️ **Database Migrations** - Automated schema management with Alembic
- 📊 **API Documentation** - Interactive Swagger/OpenAPI documentation
- 🧪 **Comprehensive Testing** - Unit and integration tests
- 🔍 **Code Quality** - Following Google Python Style Guide and Make Python Style Guide

## 🏗️ Architecture

This project follows a clean, modular architecture:

```
src/
├── auth/           # Authentication & authorization
├── authors/        # Author management
├── books/          # Book management
├── base/           # Shared utilities and base classes
└── main.py         # FastAPI application entry point
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)
- UV package manager (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/PitRella/LibraryPlatform
cd LibraryPlatform
```

### 2. Environment Setup

Create your environment configuration:

```bash
cp .env_example .env
```

Edit the `.env` file with your preferred settings:

```env
# FastAPI configuration
APP_NAME=LibraryPlatform
APP_HOST=0.0.0.0
APP_PORT=8000
APP_RELOAD=True
APP_MODE=dev

# Database configuration
DB_HOST=library_database
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=library_database

# JWT Token Configuration
TOKEN_SECRET_KEY=your-super-secret-jwt-key-here-make-it-long-and-random
TOKEN_ALGORITHM=HS256
TOKEN_ACCESS_TOKEN_EXPIRE_MINUTES=15
TOKEN_REFRESH_TOKEN_EXPIRE_DAYS=30

# Application level configuration
LOG_LEVEL=INFO
```

### 3. Launch with Docker

Start all services with a single command:

```bash
docker-compose up -d
```

This will:
- 🐘 Start PostgreSQL database
- 🔄 Automatically run database migrations
- 🚀 Launch the FastAPI application
- 🔍 Set up health checks

### 4. Verify Installation

Check that everything is running:

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs library_api

# Test the API
curl http://localhost:8000/health
```

## 📖 API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🗄️ Database Management

### Automated Migrations

Migrations run automatically when you start the application. For manual control, use the provided script:

```bash
# Apply all pending migrations
./scripts/migrate.sh upgrade

# Create a new migration
./scripts/migrate.sh revision "Add new feature"

# View migration history
./scripts/migrate.sh history

# Rollback to previous version
./scripts/migrate.sh downgrade -1

# Check current migration status
./scripts/migrate.sh current
```

### Manual Migration Commands

```bash
# Run migrations directly
docker-compose run --rm library_migrations

# Create new migration
docker-compose run --rm -e ALEMBIC_MESSAGE="Your message" library_migrations uv run alembic revision --autogenerate -m "Your message"
```

## 🛠️ Development Setup

### Local Development

For active development, you can run the application locally:

```bash
# Start only the database
docker-compose up library_database -d

# Install dependencies
uv sync

# Run migrations
./scripts/migrate.sh upgrade

# Start the development server
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality

This project follows strict code quality standards:

- **Google Python Style Guide** - For consistent, readable code
- **Make Python Style Guide** - For additional best practices
- **Ruff** - Fast Python linter and formatter
- **MyPy** - Static type checking
- **Pre-commit hooks** - Automated code quality checks

Run quality checks:

```bash
# Format code
uv run ruff format

# Lint code
uv run ruff check

# Type checking
uv run mypy src/

# Run all checks
uv run pre-commit run --all-files
```

### Testing

Run the test suite:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/unit/test_auth_services.py
```

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new author
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout and invalidate tokens

### Authors
- `POST /api/v1/authors/` - Create new author


### Books
- `GET /api/v1/books/` - List books with filtering
- `POST /api/v1/books/` - Create new book
- `GET /api/v1/books/{id}` - Get book by ID
- `PUT /api/v1/books/{id}` - Update book
- `DELETE /api/v1/books/{id}` - Delete book
- `POST /api/v1/books/import` - Bulk import books

### System
- `GET /health` - Health check endpoint

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `LibraryPlatform` |
| `APP_HOST` | Host to bind to | `0.0.0.0` |
| `APP_PORT` | Port to bind to | `8000` |
| `APP_MODE` | Application mode | `dev` |
| `DB_HOST` | Database host | `library_database` |
| `DB_PORT` | Database port | `5432` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` |
| `DB_NAME` | Database name | `library_database` |
| `TOKEN_SECRET_KEY` | JWT secret key | **Required** |
| `TOKEN_ALGORITHM` | JWT algorithm | `HS256` |
| `TOKEN_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiry | `15` |
| `TOKEN_REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry | `30` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🐳 Docker Commands

### Basic Operations

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up --build -d

# Stop and remove volumes (⚠️ Data loss!)
docker-compose down -v
```

### Service-Specific Commands

```bash
# Start only database
docker-compose up library_database -d

# Start only API
docker-compose up library_api -d

# Run migrations only
docker-compose run --rm library_migrations

# Access database shell
docker-compose exec library_database psql -U postgres -d library_database
```

## 📁 Project Structure

```
LibraryPlatform/
├── src/                    # Source code
│   ├── auth/              # Authentication module
│   ├── authors/           # Author management
│   ├── books/             # Book management
│   ├── base/              # Shared utilities
│   ├── database.py        # Database configuration
│   ├── main.py            # FastAPI app
│   └── settings.py        # Application settings
├── migrations/            # Database migrations
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── docs/                  # Documentation
├── docker-compose.yml     # Docker services
├── Dockerfile            # Container definition
├── pyproject.toml        # Project configuration
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the code style guidelines (Google Python Style Guide + Make Python Style Guide)
4. Write tests for your changes
5. Run the quality checks (`uv run pre-commit run --all-files`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Serhii Kryvtsun**
- GitHub: [@pitrella](https://github.com/pitrella)
- Telegram: [@pitrella]

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [SQLAlchemy](https://sqlalchemy.org/) - Python SQL toolkit
- [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) - Code style guidelines
- [Make Python Style Guide](https://make.readthedocs.io/en/latest/python-style-guide.html) - Additional best practices

---

⭐ **Star this repository if you find it helpful!**
