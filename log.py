# app.py
from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS, cross_origin
import datetime
import json
from app_logger import logger  # Import the configured logger

app = Flask(__name__)
CORS(app)

# Function to log data to a file
def log_to_file(req, res):
    data = {
        'request': {
            'method': req.method,
            'url': req.url,
            'headers': dict(req.headers),
            'data': req.get_data(as_text=True),
            'args': req.args.to_dict(),
            'form': req.form.to_dict()
        },
        'response': {
            'status_code': res.status_code,
            'headers': dict(res.headers),
            'data': res.get_data(as_text=True)
        },
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    logger.info(json.dumps(data))

# Middleware to log the request and response
@app.after_request
def after_request(response):
    log_to_file(request, response)
    return response

# Define your routes and view functions here
@app.route('/')
def index():
    return 'Hello, World!'

# More of your Flask app code...
# ...


import logging
from logging.handlers import RotatingFileHandler
import os

# Set up logging to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            os.path.join(os.getcwd(), 'app.log'),
            maxBytes=10000000,
            backupCount=10
        )
    ]
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


