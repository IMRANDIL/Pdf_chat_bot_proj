# vector_store.py

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader

load_dotenv()  # take environment variables from .env.
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")
# To store embeddings and documents globally


def setup_vector_store(directory_path):
    

    # Initialize Google Generative AI Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Load PDF files from the specified directory
   
    loader = PyPDFDirectoryLoader(directory_path)
    docs = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)

    # Create FAISS vector store
    vector_store = FAISS.from_documents(final_documents, embeddings)

    print("Vector store is ready.", vector_store)
    return vector_store
