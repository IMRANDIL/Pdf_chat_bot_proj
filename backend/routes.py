from flask import Blueprint, request, jsonify
import time
from retriever import generate_response
from vector_store import setup_vector_store

api_blueprint = Blueprint('api', __name__)

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
