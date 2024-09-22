from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import logging
import threading
from routes import api_blueprint
from cleanup_2_dir import schedule_cleanup  # Import the cleanup scheduler

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(api_blueprint)

# Function to start the cleanup script in a background thread
def start_cleanup_thread():
    cleanup_thread = threading.Thread(target=schedule_cleanup)
    cleanup_thread.daemon = True  # Allows Flask app to exit even if this thread is running
    cleanup_thread.start()

# Main entry point
if __name__ == "__main__":
    # Start the cleanup thread
    start_cleanup_thread()
    
    # Run the Flask app
    app.run(debug=True)
