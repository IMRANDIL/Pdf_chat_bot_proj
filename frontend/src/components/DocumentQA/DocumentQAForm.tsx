import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { fetchDocumentQA } from '../../services/api';

const DocumentQAForm: React.FC = () => {
  const [question, setQuestion] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate(); // Initialize navigate

  const handleQuestionSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetchDocumentQA(question);
      setResponse(res.answer);
    } catch (error) {
      console.error('Error asking question:', error);
    }
    setLoading(false);
  };

  const handleGoBack = () => {
    navigate('/'); // Redirects to the home screen (uploader)
  };

  return (
    <div className="qa-form-container">
      <h2>Ask a Question</h2>
      <div className="input-container">
        <input
          type="text"
          placeholder="Enter your question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={handleQuestionSubmit} disabled={loading || !question}>
          {loading ? 'Loading...' : 'Ask Question'}
        </button>
      </div>

      {response && (
        <div className="response-container">
          <h3>Response: -- </h3>
          <p>{response}</p>
        </div>
      )}

      {/* Back to Uploader Button */}
      <button className="go-back-button" onClick={handleGoBack}>
        Go Back to Uploader
      </button>
    </div>
  );
};

export default DocumentQAForm;
