from flask import Flask, jsonify, g, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["endpoint"])


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def record_metrics(response):
    duration = time.time() - g.start
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path, status=response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint=request.path).observe(duration)
    return response


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/ready")
def ready():
    return jsonify(status="ready"), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.route("/")
def index():
    return jsonify(message="monitoring service"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
