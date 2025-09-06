FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync --frozen

COPY src/ ./src/
COPY alembic.ini ./
COPY migrations/ ./migrations/

RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

EXPOSE 8000

# Create startup script
RUN echo '#!/bin/bash\nuv run uvicorn src.main:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000} --reload' > /app/start.sh && \
    chmod +x /app/start.sh

CMD ["/app/start.sh"]
