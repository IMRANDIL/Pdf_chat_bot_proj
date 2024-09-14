from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# To store embeddings and documents globally
vector_store = None

def setup_vector_store():
    global vector_store

    # Initialize Google Generative AI Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Load PDF files
    loader = PyPDFDirectoryLoader("./source")
    docs = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs[:20])  # Limit to 20 documents for now
    
    # Create FAISS vector store
    vector_store = FAISS.from_documents(final_documents, embeddings)

    print("Vector store is ready.")
