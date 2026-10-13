# ---- base: runtime dependencies + app code ----
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# ---- test: adds dev tools and tests (build with --target test) ----
FROM base AS test
COPY requirements-dev.txt .flake8 pytest.ini ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY tests ./tests
CMD ["pytest", "-v"]

# ---- runtime: small, non-root production image (default target) ----
FROM base AS runtime
RUN useradd --create-home --uid 1001 appuser
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:5000/health')" || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
