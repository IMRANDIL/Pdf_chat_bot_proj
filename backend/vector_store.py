from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Load environment variables from the .env file
load_dotenv()

# Set the Google API Key from the environment
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Function to setup the FAISS vector store
def setup_vector_store(directory_path, user_email, batch_size=10):
    """
    This function processes documents in batches, creates their embeddings, 
    and stores them in a FAISS index to avoid running out of memory.

    Parameters:
    - directory_path: The base directory path where user folders and documents are stored.
    - user_email: The email of the user to identify the correct folder.
    - batch_size: Number of documents to process in each batch.
    """
    # Initialize the embedding model using Google Generative AI
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Construct the path to the user's directory where their PDFs are stored
    user_dir = os.path.join(directory_path, user_email)
    if not os.path.exists(user_dir):
        raise ValueError(f"No directory found for the user: {user_email}")

    # Load PDF files only from the user's directory
    loader = PyPDFDirectoryLoader(user_dir)
    docs = loader.load()

    # Ensure that documents were successfully loaded
    if not docs:
        raise ValueError("No PDF files found in the user's directory.")

    # Initialize the vector store to None (it will be created when processing the first batch)
    vector_store = None
    
    # Split the loaded documents in chunks with a character length limit
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Process documents in batches
    for i in range(0, len(docs), batch_size):
        # Take a subset of the documents to process
        batch_docs = docs[i:i+batch_size]

        # Split these documents into smaller chunks
        batch_split_docs = text_splitter.split_documents(batch_docs)

        # Create or add to the FAISS vector store incrementally
        if vector_store is None:
            # Create the vector store for the first batch
            vector_store = FAISS.from_documents(batch_split_docs, embeddings)
        else:
            # Add subsequent document batches to the existing FAISS vector store
            vector_store.add_documents(batch_split_docs)

    # Once all documents are processed, return the ready vector store
    print("Vector store is ready.")
    return vector_store

# Function to save the FAISS index to a directory
def save_faiss_index(vector_store, save_path):
    """
    Save the FAISS index to disk so that it can be reused without recalculating embeddings.

    Parameters:
    - vector_store: The FAISS vector store object.
    - save_path: The directory where the FAISS index should be saved.
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    vector_store.save_local(save_path)

# Function to load the FAISS index from a directory if it exists
def load_faiss_index(save_path, embeddings):
    """
    Load the FAISS index from disk if it exists to avoid recomputation.

    Parameters:
    - save_path: The directory where the FAISS index is saved.
    - embeddings: The embeddings model to associate with the FAISS index.

    Returns:
    - The loaded FAISS vector store.
    """
    if os.path.exists(save_path):
        return FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
    else:
        raise FileNotFoundError(f"No FAISS index found at {save_path}")
