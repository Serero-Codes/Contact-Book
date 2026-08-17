# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependencies file first for layer caching
COPY backend/requirements.txt ./backend/requirements.txt

# Install dependencies using pre-compiled wheels
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r ./backend/requirements.txt

# Create a non-privileged user for security
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy application files
COPY --chown=appuser:appuser backend /app/backend
COPY --chown=appuser:appuser frontend /app/frontend
COPY --chown=appuser:appuser nginx /app/nginx

USER appuser

WORKDIR /app/backend

EXPOSE 5000

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]