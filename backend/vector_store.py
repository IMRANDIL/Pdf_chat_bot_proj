# vector_store.py

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader

load_dotenv()  # take environment variables from .env.
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
# To store embeddings and documents globally
def setup_vector_store(directory_path, user_email):
    # Initialize Google Generative AI Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Construct the path to the user's directory
    user_dir = os.path.join(directory_path, user_email)

    # Check if the user directory exists
    if not os.path.exists(user_dir):
        raise ValueError(f"No directory found for the user: {user_email}")

    # Load PDF files only from the user's directory
    loader = PyPDFDirectoryLoader(user_dir)
    docs = loader.load()

    # Check if any documents were loaded
    if not docs:
        raise ValueError("No PDF files found in the user's directory.")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)

    # Create FAISS vector store
    vector_store = FAISS.from_documents(final_documents, embeddings)

    print("Vector store is ready.", vector_store)
    return vector_store
