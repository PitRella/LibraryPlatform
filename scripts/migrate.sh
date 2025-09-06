#!/bin/bash

# Database migration management script for Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${GREEN}[MIGRATE]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check for .env file
if [ ! -f .env ]; then
    warn ".env file not found. Creating from .env_example..."
    cp .env_example .env
    warn "Please edit the .env file with your settings before continuing"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

case "${1:-upgrade}" in
    "upgrade"|"up")
        log "Applying all migrations..."
        docker-compose run --rm library_migrations
        ;;
    "downgrade"|"down")
        if [ -z "$2" ]; then
            error "Please specify revision to downgrade to. Example: ./scripts/migrate.sh downgrade -1"
            exit 1
        fi
        log "Downgrading migrations to version: $2"
        docker-compose run --rm -e ALEMBIC_REVISION="$2" library_migrations uv run alembic downgrade "$2"
        ;;
    "revision"|"rev")
        if [ -z "$2" ]; then
            error "Please specify migration message. Example: ./scripts/migrate.sh revision 'Add new table'"
            exit 1
        fi
        log "Creating new migration: $2"
        docker-compose run --rm -e ALEMBIC_MESSAGE="$2" library_migrations uv run alembic revision --autogenerate -m "$2"
        ;;
    "history"|"hist")
        log "Showing migration history..."
        docker-compose run --rm library_migrations uv run alembic history
        ;;
    "current"|"cur")
        log "Current migration version:"
        docker-compose run --rm library_migrations uv run alembic current
        ;;
    "heads"|"head")
        log "Latest migration versions:"
        docker-compose run --rm library_migrations uv run alembic heads
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command] [arguments]"
        echo ""
        echo "Commands:"
        echo "  upgrade, up                    Apply all migrations (default)"
        echo "  downgrade, down <revision>     Downgrade to specified version"
        echo "  revision, rev <message>        Create new migration"
        echo "  history, hist                  Show migration history"
        echo "  current, cur                   Show current version"
        echo "  heads, head                    Show latest versions"
        echo "  help, -h, --help               Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 upgrade                     # Apply all migrations"
        echo "  $0 downgrade -1                # Downgrade one version back"
        echo "  $0 revision 'Add user table'   # Create new migration"
        ;;
    *)
        error "Unknown command: $1"
        echo "Use '$0 help' for help"
        exit 1
        ;;
esac
