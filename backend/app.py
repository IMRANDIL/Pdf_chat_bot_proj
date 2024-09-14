from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from routes import api_blueprint

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(api_blueprint)

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
