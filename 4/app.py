import time
from flask import Flask
from prometheus_client import Gauge, generate_latest
from prometheus_client.exposition import basic_auth_handler

# Create the Flask app
app = Flask(__name__)

# Define the Prometheus metrics
INPROGRESS = Gauge('hello_worlds_inprogress', 'Number of Hello Worlds in progress.')
LAST = Gauge('hello_world_last_time_seconds', 'The last time a Hello World was served.')

@app.route('/hello', methods=['GET'])
def hello_world():
    INPROGRESS.inc()  # Increment the counter for in-progress Hello World requests
    LAST.set(time.time())  # Set the current time as the last served time
    time.sleep(1)  # Simulate some delay in processing
    INPROGRESS.dec()  # Decrement the counter after processing is done
    return "Hello World", 200

@app.route('/metrics', methods=['GET'])
def metrics():
    # Expose Prometheus metrics
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
