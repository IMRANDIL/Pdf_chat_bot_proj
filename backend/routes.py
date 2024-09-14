import os
from flask import Blueprint, request, jsonify
import time
from werkzeug.utils import secure_filename
from retriever import generate_response
from vector_store import setup_vector_store
from langchain_community.document_loaders import PyPDFLoader

UPLOAD_FOLDER = './source'  # Directory to store uploaded PDFs
ALLOWED_EXTENSIONS = {'pdf'}

api_blueprint = Blueprint('api', __name__)

# Check if the file is a PDF
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        start = time.process_time()
        response = generate_response(question)
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
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Load the PDF and process it
            loader = PyPDFLoader(filepath)
            documents = loader.load()
            
            # Embed the uploaded PDF into the vector store
            setup_vector_store(documents)

            return jsonify({"message": f"PDF '{filename}' uploaded and processed successfully."}), 200
        else:
            return jsonify({"error": "Only PDF files are allowed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
