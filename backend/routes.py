import os
import shutil
from flask import Blueprint, request, jsonify
import time
from werkzeug.utils import secure_filename
from retriever import generate_response
# from vector_store import setup_vector_store
# from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from vector_store import setup_vector_store,load_faiss_index

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



# Route to list all PDFs uploaded by a user
@api_blueprint.route('/list-docs', methods=['GET'])
def list_docs():
    try:
        # Get the email from query parameters
        user_email = request.args.get('email')
        if not user_email:
            return jsonify({"error": "No email provided"}), 400

        # Construct the user's upload directory
        user_dir = os.path.join(UPLOAD_FOLDER, user_email)
        
        # Check if the directory exists
        if not os.path.exists(user_dir):
            return jsonify({"message": "No documents found for this user."}), 200

        # Get a list of all PDF files in the user's directory
        documents = [doc for doc in os.listdir(user_dir) if doc.endswith('.pdf')]

        # Return the list of documents
        return jsonify({"documents": documents}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# Route to embed documents and create the vector store
@api_blueprint.route('/embed-documents', methods=['POST'])
def embed_documents():
    try:
        setup_vector_store()
        return jsonify({"message": "Vector Store DB is ready"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# @api_blueprint.route('/ask-question', methods=['POST'])
# def ask_question():
#     try:
#         data = request.json
#         question = data.get('question', '')
#         userEmail = data.get('userEmail', '')

#         if not question:
#             return jsonify({"error": "No question provided"}), 400

#         if not userEmail:
#             return jsonify({"error": "No user email provided"}), 400

#         # Path where FAISS index is saved
#         faiss_index_path = os.path.join(UPLOAD_FOLDER, userEmail, "faiss_index")

#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#         # Check if FAISS index exists, if not, create it
#         if not os.path.exists(faiss_index_path):
#             # Set up vector store by embedding documents
#             documents_folder = os.path.join(UPLOAD_FOLDER, userEmail, "documents")
#             vector_store = setup_vector_store(UPLOAD_FOLDER, userEmail, faiss_index_path)  # Pass faiss_index_path to save the FAISS index
#         else:
#             # Load FAISS vector store
#             vector_store = load_faiss_index(faiss_index_path, embeddings)

#         # Generate response using the loaded vector store
#         start = time.process_time()
#         response = generate_response(question, vector_store)
#         response_time = time.process_time() - start

#         return jsonify({
#             "answer": response['answer'],
#             "response_time": response_time,
#             "context": [doc.page_content for doc in response["context"]]
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500




# @api_blueprint.route('/ask-question', methods=['POST'])
# def ask_question():
#     try:
#         data = request.json
#         question = data.get('question', '')
#         userEmail = data.get('userEmail', '')
#         doc_name = data.get('doc_name', '')  # Get the document name

#         if not question:
#             return jsonify({"error": "No question provided"}), 400

#         if not userEmail:
#             return jsonify({"error": "No user email provided"}), 400

#         if not doc_name:
#             return jsonify({"error": "No document name provided"}), 400

#         # Path where FAISS index is saved for this specific document
#         faiss_index_path = os.path.join(UPLOAD_FOLDER, userEmail, f"{doc_name}_faiss_index")

#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#         # Check if FAISS index exists, if not, create it
#         if not os.path.exists(faiss_index_path):
#             # Set up vector store by embedding the selected document
#             document_path = os.path.join(UPLOAD_FOLDER, userEmail, doc_name)
#             if not os.path.exists(document_path):
#                 return jsonify({"error": f"Document '{doc_name}' not found for user '{userEmail}'"}), 404
            
#             vector_store = setup_vector_store(document_path, userEmail, faiss_index_path)  # Pass faiss_index_path to save the FAISS index
#         else:
#             # Load FAISS vector store
#             vector_store = load_faiss_index(faiss_index_path, embeddings)

#         # Generate response using the loaded vector store
#         start = time.process_time()
#         response = generate_response(question, vector_store)
#         response_time = time.process_time() - start

#         return jsonify({
#             "answer": response['answer'],
#             "response_time": response_time,
#             "context": [doc.page_content for doc in response["context"]]
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



@api_blueprint.route('/ask-question', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get('question', '')
        userEmail = data.get('userEmail', '')
        doc_name = data.get('doc_name', '')

        if not question:
            return jsonify({"error": "No question provided"}), 400

        if not userEmail:
            return jsonify({"error": "No user email provided"}), 400

        if not doc_name:
            return jsonify({"error": "No document name provided"}), 400

        # Path where FAISS index is saved for this specific document
        document_path = os.path.join(UPLOAD_FOLDER, userEmail, doc_name)
        faiss_index_path = os.path.join(UPLOAD_FOLDER, userEmail, f"{doc_name}_faiss_index")

        # Check if the document exists first
        if not os.path.exists(document_path):
            return jsonify({"error": f"Document '{doc_name}' not found for user '{userEmail}'"}), 404

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Check if FAISS index exists, if not, create it
        vector_store = None
        if os.path.exists(faiss_index_path):
            # Load FAISS vector store
            vector_store = load_faiss_index(faiss_index_path, embeddings)
        else:
            # Set up vector store by embedding the selected document
            vector_store = setup_vector_store(document_path, userEmail, faiss_index_path)

        # Generate response using the loaded vector store
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
            # loader = PyPDFLoader(filepath)
            # documents = loader.load()
            
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
