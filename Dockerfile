# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Install uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# System dependencies + SQL Server ODBC driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gnupg2 ca-certificates unixodbc-dev && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 && \
    DRIVER_PATH="$(ls /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17*.so* | head -n 1)" && \
    printf "[SQL Server]\nDescription=Microsoft ODBC Driver 17 for SQL Server (alias)\nDriver=%s\nUsageCount=1\n" "$DRIVER_PATH" >> /etc/odbcinst.ini && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first for better layer caching
COPY pyproject.toml ./
COPY uv.lock* ./
RUN uv sync --frozen --no-dev

# Copy project files
COPY . .

# Runtime default environment for main.py arg
ENV APP_ENV=hpc_dev

CMD ["sh", "-c", "uv run python main.py ${APP_ENV}"]
