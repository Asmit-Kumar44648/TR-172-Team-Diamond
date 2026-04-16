FROM python:3.11-slim
WORKDIR /app

# Install system dependencies required by Weasyprint for PDF generation
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libjpeg-dev \
    libopenjp2-7-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole monorepo context to maintain import paths
COPY apps/api/ apps/api/
COPY packages/ packages/

EXPOSE 8000
CMD ["sh", "-c", "python -m uvicorn apps.api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
