from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Load environment variables
import os
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



def generate_response(question, vector_store):
    if vector_store is None:
        raise ValueError("Vector store is not initialized. Please embed documents first.")
    
    # Create the document chain for LLM
    document_chain = create_stuff_documents_chain(llm, prompt_template)
    
    # Create a retriever from the vector store
    retriever = vector_store.as_retriever()
    
    # Create retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    # Get the response for the user question
    response = retrieval_chain.invoke({'input': question})
    
    return response
