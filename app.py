from flask import Flask, request, jsonify
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import start_http_server
import random
import time

app = Flask(__name__)

# Define Prometheus metrics with updated names
count_of_http_requests = Counter('count_of_http_requests', 'Count of total HTTP requests', ['method', 'endpoint'])
gauge_memory_utilization_bytes = Gauge('gauge_memory_utilization_bytes', 'Simulated memory utilization in bytes')

# New Histogram with the custom name 'historam_duration_req'
historam_duration_req = Histogram(
    'historam_duration_req', 
    'Histogram of HTTP request durations in seconds', 
    ['method', 'endpoint'],
    buckets=[0.1, 0.3, 0.5, 1.0, 2.0, 5.0]  # Buckets for request duration
)

# Endpoint to serve metrics
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Simulated endpoints
@app.route('/simulate_get', methods=['GET'])
def simulate_get():
    start_time = time.time()  # Start timer
    count_of_http_requests.labels(method='GET', endpoint='/simulate_get').inc()
    time.sleep(random.uniform(0.1, 0.5))  # Simulate processing time
    duration = time.time() - start_time  # Calculate request duration
    historam_duration_req.labels(method='GET', endpoint='/simulate_get').observe(duration)
    return jsonify(message="GET request simulated!", duration=f"{duration:.2f} seconds")

@app.route('/simulate_post', methods=['POST'])
def simulate_post():
    start_time = time.time()  # Start timer
    count_of_http_requests.labels(method='POST', endpoint='/simulate_post').inc()
    time.sleep(random.uniform(0.2, 0.8))  # Simulate processing time
    duration = time.time() - start_time  # Calculate request duration
    historam_duration_req.labels(method='POST', endpoint='/simulate_post').observe(duration)
    return jsonify(message="POST request simulated!", duration=f"{duration:.2f} seconds")

@app.route('/simulate_memory', methods=['GET'])
def simulate_memory():
    # Simulate random memory usage
    current_memory = random.randint(400, 800) * 1024 * 1024  # Memory in bytes
    gauge_memory_utilization_bytes.set(current_memory)
    return jsonify(memory_usage=current_memory)

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(8001)  # Prometheus metrics available at http://localhost:8001/metrics
    print("Prometheus metrics available on /metrics endpoint")
    app.run(debug=True, port=5000)

