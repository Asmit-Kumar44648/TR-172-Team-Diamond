FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for any packages that might need them (e.g. build-essential if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy internal packages first to /app/packages to match monorepo relative paths
COPY packages/pipeline/ /app/packages/pipeline/
COPY packages/schema/ /app/packages/schema/
COPY packages/agents/ /app/packages/agents/

# Copy API source
COPY apps/api/ /app/

# Expose FastAPI port
EXPOSE 8000

# Set PYTHONPATH so 'packages.pipeline' etc. are importable
ENV PYTHONPATH=/app

# Deployment command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
