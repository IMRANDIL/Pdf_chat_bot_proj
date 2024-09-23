# from langchain_community.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFDirectoryLoader

# # Load environment variables from the .env file
# load_dotenv()

# # Set the Google API Key from the environment
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# # Function to setup the FAISS vector store
# def setup_vector_store(directory_path, user_email, batch_size=10):
#     """
#     This function processes documents in batches, creates their embeddings, 
#     and stores them in a FAISS index to avoid running out of memory.

#     Parameters:
#     - directory_path: The base directory path where user folders and documents are stored.
#     - user_email: The email of the user to identify the correct folder.
#     - batch_size: Number of documents to process in each batch.
#     """
#     # Initialize the embedding model using Google Generative AI
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     # Construct the path to the user's directory where their PDFs are stored
#     user_dir = os.path.join(directory_path, user_email)
#     if not os.path.exists(user_dir):
#         raise ValueError(f"No directory found for the user: {user_email}")

#     # Load PDF files only from the user's directory
#     loader = PyPDFDirectoryLoader(user_dir)
#     docs = loader.load()

#     # Ensure that documents were successfully loaded
#     if not docs:
#         raise ValueError("No PDF files found in the user's directory.")

#     # Initialize the vector store to None (it will be created when processing the first batch)
#     vector_store = None
    
#     # Split the loaded documents in chunks with a character length limit
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

#     # Process documents in batches
#     for i in range(0, len(docs), batch_size):
#         # Take a subset of the documents to process
#         batch_docs = docs[i:i+batch_size]

#         # Split these documents into smaller chunks
#         batch_split_docs = text_splitter.split_documents(batch_docs)

#         # Create or add to the FAISS vector store incrementally
#         if vector_store is None:
#             # Create the vector store for the first batch
#             vector_store = FAISS.from_documents(batch_split_docs, embeddings)
#         else:
#             # Add subsequent document batches to the existing FAISS vector store
#             vector_store.add_documents(batch_split_docs)

#     # Once all documents are processed, return the ready vector store
#     print("Vector store is ready.")
#     return vector_store

# # Function to save the FAISS index to a directory
# def save_faiss_index(vector_store, save_path):
#     """
#     Save the FAISS index to disk so that it can be reused without recalculating embeddings.

#     Parameters:
#     - vector_store: The FAISS vector store object.
#     - save_path: The directory where the FAISS index should be saved.
#     """
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     vector_store.save_local(save_path)

# # Function to load the FAISS index from a directory if it exists
# def load_faiss_index(save_path, embeddings):
#     """
#     Load the FAISS index from disk if it exists to avoid recomputation.

#     Parameters:
#     - save_path: The directory where the FAISS index is saved.
#     - embeddings: The embeddings model to associate with the FAISS index.

#     Returns:
#     - The loaded FAISS vector store.
#     """
#     if os.path.exists(save_path):
#         return FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
#     else:
#         raise FileNotFoundError(f"No FAISS index found at {save_path}")


# import chromadb
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from chromadb.config import Settings

# # Load environment variables from the .env file
# load_dotenv()

# # Set the Google API Key from the environment
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# # Initialize the ChromaDB client with persistence
# client = chromadb.Client(Settings(
#     chroma_db_impl="sqlite",  # You can switch to 'postgres' if using PostgreSQL
#     persist_directory="./chroma_storage"  # Path where vectors will be stored
# ))

# # Function to setup the ChromaDB vector store
# def setup_vector_store(directory_path, user_email, batch_size=10):
#     """
#     This function processes documents in batches, creates their embeddings, 
#     and stores them in a ChromaDB index for efficient querying.

#     Parameters:
#     - directory_path: The base directory path where user folders and documents are stored.
#     - user_email: The email of the user to identify the correct folder.
#     - batch_size: Number of documents to process in each batch.
#     """
#     # Initialize the embedding model using Google Generative AI
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     # Construct the path to the user's directory where their PDFs are stored
#     user_dir = os.path.join(directory_path, user_email)
#     if not os.path.exists(user_dir):
#         raise ValueError(f"No directory found for the user: {user_email}")

#     # Load PDF files only from the user's directory
#     loader = PyPDFDirectoryLoader(user_dir)
#     docs = loader.load()

#     # Ensure that documents were successfully loaded
#     if not docs:
#         raise ValueError("No PDF files found in the user's directory.")

#     # Split the loaded documents into smaller chunks
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     batch_split_docs = text_splitter.split_documents(docs)

#     # Create embeddings and add them to the ChromaDB collection
#     collection_name = f"user_docs_{user_email}"
#     collection = client.create_collection(name=collection_name)

#     # Add document chunks and embeddings to the collection
#     for doc in batch_split_docs:
#         vector = embeddings.embed_text(doc.page_content)
#         collection.add(
#             ids=[doc.metadata.get("doc_id", f"{user_email}_{doc.metadata.get('doc_num', 0)}")],
#             embeddings=[vector],
#             metadatas=[{"page_content": doc.page_content}]
#         )

#     print("Vector store is ready.")
#     return collection

# # Function to load the ChromaDB collection
# def load_chroma_collection(user_email):
#     """
#     Load an existing ChromaDB collection for the user.

#     Parameters:
#     - user_email: The email of the user to load the collection for.

#     Returns:
#     - The ChromaDB collection object.
#     """
#     collection_name = f"user_docs_{user_email}"
#     if client.has_collection(name=collection_name):
#         return client.get_collection(name=collection_name)
#     else:
#         raise FileNotFoundError(f"No ChromaDB collection found for {user_email}")



# import chromadb
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from chromadb.config import Settings

# # Load environment variables from the .env file
# load_dotenv()

# # Set the Google API Key from the environment
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# # Initialize the ChromaDB client with persistence
# client = chromadb.Client(Settings(
#     chroma_db_impl="sqlite",  # You can switch to 'postgres' if using PostgreSQL
#     persist_directory="./chroma_storage"  # Path where vectors will be stored
# ))

# # Function to setup the ChromaDB vector store
# def setup_vector_store(directory_path, user_email, batch_size=10):
#     """
#     This function processes documents in batches, creates their embeddings, 
#     and stores them in a ChromaDB index for efficient querying.

#     Parameters:
#     - directory_path: The base directory path where user folders and documents are stored.
#     - user_email: The email of the user to identify the correct folder.
#     - batch_size: Number of documents to process in each batch.
#     """
#     # Initialize the embedding model using Google Generative AI
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     # Construct the path to the user's directory where their PDFs are stored
#     user_dir = os.path.join(directory_path, user_email)
#     if not os.path.exists(user_dir):
#         raise ValueError(f"No directory found for the user: {user_email}")

#     # Load PDF files only from the user's directory
#     loader = PyPDFDirectoryLoader(user_dir)
#     docs = loader.load()

#     # Ensure that documents were successfully loaded
#     if not docs:
#         raise ValueError("No PDF files found in the user's directory.")

#     # Split the loaded documents into smaller chunks
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     batch_split_docs = text_splitter.split_documents(docs)

#     # Create embeddings and add them to the ChromaDB collection
#     collection_name = f"user_docs_{user_email}"
#     collection = client.create_collection(name=collection_name)

#     # Add document chunks and embeddings to the collection
#     for doc in batch_split_docs:
#         vector = embeddings.embed_text(doc.page_content)
#         collection.add(
#             ids=[doc.metadata.get("doc_id", f"{user_email}_{doc.metadata.get('doc_num', 0)}")],
#             embeddings=[vector],
#             metadatas=[{"page_content": doc.page_content}]
#         )

#     print("Vector store is ready.")
#     return collection

# # Function to load the ChromaDB collection
# def load_chroma_collection(user_email):
#     """
#     Load an existing ChromaDB collection for the user.

#     Parameters:
#     - user_email: The email of the user to load the collection for.

#     Returns:
#     - The ChromaDB collection object.
#     """
#     collection_name = f"user_docs_{user_email}"
#     if client.has_collection(name=collection_name):
#         return client.get_collection(name=collection_name)
#     else:
#         raise FileNotFoundError(f"No ChromaDB collection found for {user_email}")



import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
import re
import logging

# Load environment variables from the .env file
load_dotenv()

# Set the Google API Key from the environment
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to initialize Chroma clients
# def initialize_clients():
#     """Initialize Chroma clients."""
#     try:
#         chroma_client = chromadb.Client()  # Temporary client
#         chroma_persistent_client = chromadb.PersistentClient("source_croma_db")  # Persistent client
#         return chroma_client, chroma_persistent_client
#     except Exception as e:
#         logging.error(f"Error initializing Chroma clients: {e}")
#         raise

# # Initialize clients
# chroma_client, chroma_persistent_client = initialize_clients()

# Function to sanitize the collection name
def sanitize_collection_name(email):
    """Sanitize the user email for use as a collection name."""
    sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', email)  # Replace invalid characters
    sanitized_name = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', sanitized_name)  # Ensure alphanumeric start/end
    return f"user_docs_{sanitized_name}"

# Function to setup the ChromaDB vector store
# def setup_vector_store(directory_path, user_email, batch_size=10):
#     """Setup ChromaDB vector store."""
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
#     user_dir = os.path.join(directory_path, user_email)
#     if not os.path.exists(user_dir):
#         raise ValueError(f"No directory found for the user: {user_email}")

#     loader = PyPDFDirectoryLoader(user_dir)
#     docs = loader.load()
    
#     if not docs:
#         raise ValueError("No PDF files found in the user's directory.")

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     batch_split_docs = text_splitter.split_documents(docs)

#     # Sanitize the user email for the collection name
#     collection_name = sanitize_collection_name(user_email)
#     collection = chroma_persistent_client.get_or_create_collection(collection_name)

#     # Prepare lists to hold documents, embeddings, metadata, and ids
#     document_contents = []
#     embeddings_list = []
#     metadatas = []
#     ids = []

#     for doc in batch_split_docs:
#         try:
#             vector = embeddings.embed_query(doc.page_content)  # Change this line
#             document_contents.append(doc.page_content)
#             embeddings_list.append(vector)
#             metadatas.append({"page_content": doc.page_content})
#             # Ensure that doc.metadata is not None
#             if doc.metadata is not None:
#                 ids.append(doc.metadata.get("doc_id", f"{user_email}_{doc.metadata.get('doc_num', 0)}"))
#             else:
#                 logging.warning("Document metadata is None. Generating ID based on email.")
#                 ids.append(f"{user_email}_{len(ids)}")  # Fallback ID generation
#             # ids.append(doc.metadata.get("doc_id", f"{user_email}_{doc.metadata.get('doc_num', 0)}"))
#         except Exception as e:
#             logging.error(f"Error processing document: {e}")

#     # Add all at once
#     collection.add(
#         documents=document_contents,
#         embeddings=embeddings_list,
#         metadatas=metadatas,
#         ids=ids
#     )

#     logging.info("Vector store is ready.")
#     return collection


# def setup_vector_store(directory_path, user_email, batch_size=10):
#     """Setup ChromaDB vector store."""
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  
    
#     user_dir = os.path.join(directory_path, user_email)
#     if not os.path.exists(user_dir):
#         raise ValueError(f"No directory found for the user: {user_email}")

#     loader = PyPDFDirectoryLoader(user_dir)
#     docs = loader.load()
    
#     if not docs:
#         raise ValueError("No PDF files found in the user's directory.")

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     batch_split_docs = text_splitter.split_documents(docs)

#     # Sanitize the user email for the collection name
#     collection_name = sanitize_collection_name(user_email)
#     collection = chroma_persistent_client.get_or_create_collection(collection_name)

#     # Prepare lists to hold documents, embeddings, metadata, and ids
#     document_contents = []
#     embeddings_list = []
#     metadatas = []
#     ids = []

#     existing_ids = set()  # To track existing IDs

#     for doc in batch_split_docs:
#         try:
#             vector = embeddings.embed_query(doc.page_content)  # Adjusted to use the corrected embedding model
#             document_contents.append(doc.page_content)
#             embeddings_list.append(vector)
#             metadatas.append({"page_content": doc.page_content})

#             # Generate a unique ID
#             base_id = doc.metadata.get("doc_id", f"{user_email}_{len(ids)}")
#             unique_id = base_id

#             # Ensure uniqueness by appending a counter if necessary
#             counter = 1
#             while unique_id in existing_ids:
#                 unique_id = f"{base_id}_{counter}"
#                 counter += 1

#             existing_ids.add(unique_id)
#             ids.append(unique_id)

#         except Exception as e:
#             logging.error(f"Error processing document: {e}")

#     # Add all at once
#     collection.add(
#         documents=document_contents,
#         embeddings=embeddings_list,
#         metadatas=metadatas,
#         ids=ids
#     )

#     logging.info("Vector store is ready.")
#     return collection



# from langchain_community.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFDirectoryLoader

# # Load environment variables from the .env file
# load_dotenv()

# # Set the Google API Key from the environment
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# # Function to setup the FAISS vector store with disk storage
# def setup_vector_store(directory_path, user_email, save_path, batch_size=10):
#     """
#     This function processes documents in batches, creates their embeddings, 
#     and stores them in a FAISS index that is saved to disk for reuse.
#     """
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     user_dir = os.path.join(directory_path, user_email)
#     if not os.path.exists(user_dir):
#         raise ValueError(f"No directory found for the user: {user_email}")

#     loader = PyPDFDirectoryLoader(user_dir)
#     docs = loader.load()

#     if not docs:
#         raise ValueError("No PDF files found in the user's directory.")

#     vector_store = None
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

#     for i in range(0, len(docs), batch_size):
#         batch_docs = docs[i:i+batch_size]
#         batch_split_docs = text_splitter.split_documents(batch_docs)

#         if vector_store is None:
#             vector_store = FAISS.from_documents(batch_split_docs, embeddings)
#         else:
#             vector_store.add_documents(batch_split_docs)

#     # Save FAISS index to the specified path
#     save_faiss_index(vector_store, save_path)

#     print("Vector store is ready and saved to disk.")
#     return vector_store

# # Function to save the FAISS index to a directory
# def save_faiss_index(vector_store, save_path):
#     """
#     Save the FAISS index to disk so that it can be reused without recalculating embeddings.

#     Parameters:
#     - vector_store: The FAISS vector store object.
#     - save_path: The directory where the FAISS index should be saved.
#     """
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     vector_store.save_local(save_path)

# # Function to load the FAISS index from a directory if it exists
# def load_faiss_index(save_path, embeddings):
#     """
#     Load the FAISS index from disk if it exists to avoid recomputation.

#     Parameters:
#     - save_path: The directory where the FAISS index is saved.
#     - embeddings: The embeddings model to associate with the FAISS index.

#     Returns:
#     - The loaded FAISS vector store.
#     """
#     if os.path.exists(save_path):
#         return FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
#     else:
#         raise FileNotFoundError(f"No FAISS index found at {save_path}")




from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

# Load environment variables from the .env file
load_dotenv()

# Set the Google API Key from the environment
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Function to setup the FAISS vector store with disk storage for a specific document
def setup_vector_store(document_path, user_email, save_path, batch_size=10):
    """
    This function processes a specific document, creates its embeddings, 
    and stores them in a FAISS index that is saved to disk for reuse.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    if not os.path.exists(document_path):
        raise ValueError(f"No document found at path: {document_path}")

    loader = PyPDFLoader(document_path)
    docs = loader.load()

    if not docs:
        raise ValueError(f"No valid content found in the document: {document_path}")

    vector_store = None
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Split document content into chunks
    split_docs = text_splitter.split_documents(docs)

    # Create FAISS index from document chunks
    vector_store = FAISS.from_documents(split_docs, embeddings)

    # Save FAISS index to the specified path
    save_faiss_index(vector_store, save_path)

    print(f"Vector store for {document_path} is ready and saved to disk.")
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
