FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY requirements.lock ./
RUN python -m pip install --require-hashes --requirement requirements.lock

COPY --chown=appuser:appuser med_sync_app.py ./
COPY --chown=appuser:appuser medsync ./medsync
COPY --chown=appuser:appuser .streamlit ./.streamlit

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=3)"

CMD ["streamlit", "run", "med_sync_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
