# HSRI 2.0 Engine Core REST API
FROM python:3.10-slim

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     curl     && rm -rf /var/lib/apt/lists/*

# Copy engine packages and data
COPY pyproject.toml /app/
COPY hsri_engine /app/hsri_engine
COPY scripts /app/scripts
COPY data /app/data

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic \
    numpy \
    pandas \
    scipy \
    requests

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["uvicorn", "hsri_engine.api:app", "--host", "0.0.0.0", "--port", "8000"]
