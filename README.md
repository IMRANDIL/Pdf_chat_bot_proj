# Document Q&A System

This project is a full-stack Document Q&A system that allows users to ask questions about uploaded documents and receive accurate, content-based responses. The system consists of a React + TypeScript frontend and a Flask-based backend. 

The backend uses advanced AI libraries like Langchain, FAISS, and Groq for efficient document processing and retrieval. The frontend allows users to ask questions and display results in an intuitive interface.

## Features

- **AI-Powered Q&A**: Ask questions about uploaded documents and get precise answers based on the content.
- **Document Embedding**: Efficient document embeddings using FAISS for fast document retrieval.
- **PDF Support**: Load PDF documents for analysis and question answering.
- **Google and Groq API Integration**: Embeddings and language models powered by Google AI and Groq.
- **Full-Stack Solution**: Frontend built with Vite, React, and TypeScript, and backend powered by Flask.

---

## Tech Stack

### Frontend
- **React** with **TypeScript** (modularized for easy scalability)
- **Vite** for fast development and production builds
- **CSS Modules** for styling components

### Backend
- **Flask**: Python micro-framework for building the API
- **FAISS**: Vector search for document retrieval
- **Langchain**: For question answering and language model integration
- **Groq**: Model for generating responses
- **Google Cloud AI**: Embedding API for document embedding
- **PyPDF2**: PDF loading and processing

---

## Getting Started

### Prerequisites

Ensure you have the following installed:
- **Node.js** (>=14.x)
- **Python** (>=3.8)
- **Google Cloud API Key** and **Groq API Key**

### Backend Setup

1. Clone the repository and navigate to the backend directory:

   ```bash
   git clone https://github.com/yourusername/document-qa.git
   cd document-qa/backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   - Create a `.env` file in the backend directory and add your API keys:

     ```
     GROQ_API_KEY=your_groq_api_key
     GOOGLE_API_KEY=your_google_api_key
     ```

5. Run the Flask server:

   ```bash
   flask run
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd ../frontend
   ```

2. Install the required Node.js packages:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

The frontend should now be running on `http://localhost:5173` and the backend API on `http://localhost:5000`.

