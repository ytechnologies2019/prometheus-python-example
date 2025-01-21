from flask import Flask, render_template
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)

@app.route('/')
def main_route():
    # Increment the request counter each time this endpoint is hit
    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status='200').inc()
    return render_template('index.html')

# Optional: Expose a metrics endpoint for Prometheus scraping
@app.route('/metrics')
def metrics():
    return generate_latest(REQUEST_COUNT), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

