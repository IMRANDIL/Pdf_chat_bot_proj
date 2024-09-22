import axios from 'axios';

const api_end_point = 'https://pdf-chat-bot-proj.onrender.com'

// API to upload PDF file
export const uploadPDF = async (file: File, userEmail: string) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('email', userEmail);

  const response = await axios.post(`http://localhost:5000/upload-pdf`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return {status: response.status, data: response.data};
};

// API to ask a question about the uploaded PDF
export const fetchDocumentQA = async (question: string) => {
  const response = await axios.post(`http://localhost:5000/ask-question`, {
    question,
  });
  return response.data;
};
