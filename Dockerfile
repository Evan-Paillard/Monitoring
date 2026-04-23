FROM python:3.12-slim AS builder

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

RUN useradd --uid 1000 --no-create-home --shell /bin/false appuser

WORKDIR /app
COPY --from=builder /install /usr/local
COPY app/ .

USER appuser

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "30", "--worker-tmp-dir", "/tmp", "main:app"]
