import axios from 'axios';

export const fetchDocumentQA = async (question: string) => {
  const response = await axios.post('http://localhost:5000/generate-email', {
    question,
  });
  return response.data;
};
