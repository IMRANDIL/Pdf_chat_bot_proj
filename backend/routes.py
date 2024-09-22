import os
import shutil
from flask import Blueprint, request, jsonify
import time
from werkzeug.utils import secure_filename
from retriever import generate_response
from vector_store import setup_vector_store
from langchain_community.document_loaders import PyPDFLoader

UPLOAD_FOLDER = './source'  # Directory to store uploaded PDFs
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

api_blueprint = Blueprint('api', __name__)

# Check if the file is a PDF
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route to check if the server is live
@api_blueprint.route('/', methods=['GET'])
def live():
    return "It's live now!", 200

# Route to embed documents and create the vector store
@api_blueprint.route('/embed-documents', methods=['POST'])
def embed_documents():
    try:
        setup_vector_store()
        return jsonify({"message": "Vector Store DB is ready"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to process user query and retrieve the response
@api_blueprint.route('/ask-question', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get('question', '')
        userEmail = data.get('userEmail', '')
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        if not userEmail:
            return jsonify({"error": "No user email provided"}), 400
        
        # Setup the vector store by loading and embedding documents
        vector_store = setup_vector_store(UPLOAD_FOLDER, userEmail)
        
        start = time.process_time()
        response = generate_response(question, vector_store)
        response_time = time.process_time() - start
        return jsonify({
            "answer": response['answer'],
            "response_time": response_time,
            "context": [doc.page_content for doc in response["context"]]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to upload PDF file
@api_blueprint.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        # Get the email from form data
        user_email = request.form.get('email')
        if not user_email:
            return jsonify({"error": "No email provided"}), 400
        
        # Create a directory for the email if it doesn't exist
        user_dir = os.path.join(UPLOAD_FOLDER, user_email)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        
        # If user does not select file
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Check if the file is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(user_dir, filename)  # Save file in the user's directory
            file.save(filepath)
            
            # Load the PDF and process it
            loader = PyPDFLoader(filepath)
            documents = loader.load()
            
            return jsonify({"message": f"PDF '{filename}' uploaded to '{user_dir}' successfully."}), 200
        else:
            return jsonify({"error": "Only PDF files are allowed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to clean the UPLOAD_FOLDER
@api_blueprint.route('/clean-upload-folder', methods=['GET'])
def clean_upload_folder():
    try:
        for root, dirs, files in os.walk(UPLOAD_FOLDER):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
        return jsonify({"message": "Upload folder cleaned successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
