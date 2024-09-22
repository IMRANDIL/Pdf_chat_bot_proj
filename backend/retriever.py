# from langchain_groq import ChatGroq
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import create_retrieval_chain

# from dotenv import load_dotenv

# load_dotenv()  # take environment variables from .env.

# # Load environment variables
# import os
# groq_api_key = os.getenv('GROQ_API_KEY')


# # Initialize LLM
# llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# # Define prompt template
# prompt_template = ChatPromptTemplate.from_template(
#     """
#     Answer the questions based on the provided context only.
#     Please provide the most accurate response based on the question.
#     <context>
#     {context}
#     <context>
#     Questions: {input}
#     """
# )



# def generate_response(question, vector_store):
#     if vector_store is None:
#         raise ValueError("Vector store is not initialized. Please embed documents first.")
    
#     # Create the document chain for LLM
#     document_chain = create_stuff_documents_chain(llm, prompt_template)
    
#     # Create a retriever from the vector store
#     retriever = vector_store.as_retriever()
    
#     # Create retrieval chain
#     retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
#     # Get the response for the user question
#     response = retrieval_chain.invoke({'input': question})
    
#     return response


# from langchain_groq import ChatGroq
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import create_retrieval_chain

# from dotenv import load_dotenv

# load_dotenv()  # take environment variables from .env.

# # Load environment variables
# import os
# groq_api_key = os.getenv('GROQ_API_KEY')

# # Initialize LLM
# llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# # Define prompt template
# prompt_template = ChatPromptTemplate.from_template(
#     """
#     Answer the questions based on the provided context only.
#     Please provide the most accurate response based on the question.
#     <context>
#     {context}
#     <context>
#     Questions: {input}
#     """
# )

# def generate_response(question, vector_store):
#     if vector_store is None:
#         raise ValueError("Vector store is not initialized. Please embed documents first.")
    
#     # Create the document chain for LLM
#     document_chain = create_stuff_documents_chain(llm, prompt_template)
    
#     # ChromaDB collection acts as the retriever
#     retriever = vector_store
    
#     # Create retrieval chain
#     retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
#     # Get the response for the user question
#     response = retrieval_chain.invoke({'input': question})
    
#     return response


from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains import RetrievalQA

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

# Load environment variables
groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize LLM
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Define prompt template
prompt_template = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Questions: {input}
    """
)

# def generate_response(question, collection):
#     if collection is None:
#         raise ValueError("Collection is not initialized. Please embed documents first.")

#     # Create a retriever from the collection with specified search type and parameters
#     retriever = collection.as_retriever(
#         search_type="mmr",  # Use Maximum Marginal Relevance for better context selection
#         search_kwargs={"k": 1, "fetch_k": 5}  # Fetch top 5 results but return 1
#     )

#     # Create the document chain for LLM
#     document_chain = create_stuff_documents_chain(llm, prompt_template)

#     # Create retrieval chain
#     retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
#     # Get the response for the user question
#     response = retrieval_chain.invoke({'input': question})
    
#     return response

def generate_response(question, collection):
    if collection is None:
        raise ValueError("Collection is not initialized. Please embed documents first.")

    # Perform a query on the collection to retrieve relevant documents
    results = collection.query(
        query_texts=[question],  # Embed the question
        n_results=5  # Adjust the number of results as needed
    )

    # Check if any documents were retrieved
    if not results or not results['documents']:
        return {"answer": "No relevant documents found.", "context": []}

    # Create the document chain for LLM
    document_chain = create_stuff_documents_chain(llm, prompt_template)

    # Prepare the context for LLM from the retrieved documents
    context = [doc.page_content for doc in results['documents']]  # Extract page content

    # Generate a response using the document chain and the question
    response = document_chain.invoke({"input": question, "context": context})

    return response
