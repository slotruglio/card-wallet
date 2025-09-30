FROM python:3.13-slim

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy project metadata first (for caching)
COPY pyproject.toml ./
# Install dependencies
RUN uv pip install --system .

# Copy source code
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
