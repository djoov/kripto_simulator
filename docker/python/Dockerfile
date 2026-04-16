FROM python:3.11-slim

# ── System dependencies ──
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

# ── Working directory ──
WORKDIR /app

# ── Install Python dependencies ──
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application source ──
COPY . .

# ── Expose port ──
EXPOSE 8001

# ── Health check ──
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/')" || exit 1

# ── Start FastAPI with Uvicorn ──
CMD ["uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8001", \
     "--workers", "2", \
     "--log-level", "info"]
