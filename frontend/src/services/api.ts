import axios from 'axios';

const api_end_point = 'https://pdf-chat-bot-proj.onrender.com'
// const api_end_point_local = 'http://localhost:5000'

// API to upload PDF file
export const uploadPDF = async (file: File, userEmail: string) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('email', userEmail);

  const response = await axios.post(`${api_end_point}/upload-pdf`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return {status: response.status, data: response.data};
};

// API to ask a question about the uploaded PDF
export const fetchDocumentQA = async (question: string, userEmail: string, doc_name: string) => {
  const response = await axios.post(`${api_end_point}/ask-question`, {
    question,
    userEmail,
    doc_name,
  });
  return response.data;
};


// API to list all PDFs uploaded by a user
export const listDocuments = async (userEmail: string) => {
  try {
    const response = await axios.get(`${api_end_point}/list-docs`, {
      params: { email: userEmail },
    });
    return response.data; // Returns the list of documents
  } catch (error) {
    console.error("Error fetching documents:", error);
    throw error; // Re-throw error for further handling if needed
  }
};
