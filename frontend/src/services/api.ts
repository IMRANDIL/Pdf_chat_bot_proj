import axios from 'axios';

const api_end_point = 'https://pdf-chat-bot-proj.onrender.com'

// API to upload PDF file
export const uploadPDF = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${api_end_point}/upload-pdf`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return {status: response.status, data: response.data};
};

// API to ask a question about the uploaded PDF
export const fetchDocumentQA = async (question: string) => {
  const response = await axios.post(`${api_end_point}/ask-question`, {
    question,
  });
  return response.data;
};
