import random
from flask import Flask
from prometheus_client import Counter

# Initialize Flask app
app = Flask(__name__)

# Define Prometheus counters
REQUESTS = Counter('hello_worlds_total', 'Hello Worlds requested.')
SALES = Counter('hello_world_sales_euro_total', 'Euros made serving Hello World.')

@app.route('/')
def hello_world():
    # Increment the request counter
    REQUESTS.inc()
    
    # Generate a random sales value in euros
    euros = random.random()
    
    # Increment the sales counter by the generated amount
    SALES.inc(euros)
    
    # Return the response
    return f"Hello World for {euros} euros."

# Optional: Expose a /metrics endpoint for Prometheus scraping
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
