import os
import shutil
from flask import Blueprint, request, jsonify
import time
from werkzeug.utils import secure_filename
from retriever import generate_response
# from vector_store import setup_vector_store
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from vector_store import setup_vector_store

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

# # Route to process user query and retrieve the response
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
        
#         # Setup the vector store by loading and embedding documents
#         vector_store = setup_vector_store(UPLOAD_FOLDER, userEmail)
        
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
#     """
#     API endpoint that takes a user's question and returns an answer based on the user's
#     PDF documents, processed through FAISS vector store for similarity-based retrieval.
#     """
#     try:
#         # Extract data from the request
#         data = request.json
#         question = data.get('question', '')
#         userEmail = data.get('userEmail', '')

#         # Validate inputs
#         if not question:
#             return jsonify({"error": "No question provided"}), 400
#         if not userEmail:
#             return jsonify({"error": "No user email provided"}), 400
        
#         # Path to the user's FAISS index
#         faiss_index_path = os.path.join(UPLOAD_FOLDER, userEmail, 'faiss_index')

#         # Initialize embeddings model
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
#         # Load FAISS index if it exists, otherwise create it
#         if os.path.exists(faiss_index_path):
#             # Load the FAISS index from disk
#             vector_store = load_faiss_index(faiss_index_path, embeddings)
#         else:
#             # Set up the vector store and save it
#             vector_store = setup_vector_store(UPLOAD_FOLDER, userEmail)
#             save_faiss_index(vector_store, faiss_index_path)

#         # Generate a response from the vector store using the question
#         start = time.process_time()
#         response = generate_response(question, vector_store)
#         response_time = time.process_time() - start

#         # Return the generated response, the context, and the response time
#         return jsonify({
#             "answer": response['answer'],
#             "response_time": response_time,
#             "context": [doc.page_content for doc in response["context"]]
#         }), 200
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @api_blueprint.route('/ask-question', methods=['POST'])
# def ask_question():
#     """
#     API endpoint that takes a user's question and returns an answer based on the user's
#     PDF documents, processed through ChromaDB for similarity-based retrieval.
#     """
#     try:
#         # Extract data from the request
#         data = request.json
#         question = data.get('question', '')
#         userEmail = data.get('userEmail', '')

#         # Validate inputs
#         if not question:
#             return jsonify({"error": "No question provided"}), 400
#         if not userEmail:
#             return jsonify({"error": "No user email provided"}), 400

#         # Initialize embeddings model
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#         # Load ChromaDB collection if it exists, otherwise create it
#         try:
#             vector_store = load_chroma_collection(userEmail)
#         except FileNotFoundError:
#             # If no collection exists, set up the vector store and save it
#             vector_store = setup_vector_store(UPLOAD_FOLDER, userEmail)

#         # Generate a response from the vector store using the question
#         query_vector = embeddings.embed_text(question)
#         results = vector_store.query(query_embeddings=[query_vector], n_results=5)

#         # Prepare the response based on the retrieved documents
#         response = {
#             'answer': results['documents'][0]['page_content'] if results['documents'] else "No relevant documents found.",
#             'context': [doc['page_content'] for doc in results['documents']]
#         }

#         return jsonify(response), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@api_blueprint.route('/ask-question', methods=['POST'])
def ask_question():
    """
    API endpoint that takes a user's question and returns an answer based on the user's
    PDF documents, processed through ChromaDB vector store for similarity-based retrieval.
    """
    try:
        # Extract data from the request
        data = request.json
        question = data.get('question', '')
        userEmail = data.get('userEmail', '')

        # Validate inputs
        if not question:
            return jsonify({"error": "No question provided"}), 400
        if not userEmail:
            return jsonify({"error": "No user email provided"}), 400
        
        # Load or setup the ChromaDB collection for the user
   
        # Load or setup the ChromaDB collection for the user
        collection = setup_vector_store(UPLOAD_FOLDER, userEmail)
    
        # Create a retriever from the collection
        # retriever = collection.as_retriever(
        #     search_type="mmr",
        #     search_kwargs={"k": 1, "fetch_k": 5}
        # )

        # Generate a response from the vector store using the question
        start = time.process_time()
        response = generate_response(question, collection)
        response_time = time.process_time() - start

        # Return the generated response, the context, and the response time
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
