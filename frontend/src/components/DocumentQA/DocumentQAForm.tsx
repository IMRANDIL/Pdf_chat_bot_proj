import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { fetchDocumentQA } from '../../services/api';
import { toast } from 'react-toastify';
import { useUser } from '@clerk/clerk-react'


const DocumentQAForm: React.FC = () => {
  const [question, setQuestion] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [showWaitMessage, setShowWaitMessage] = useState<boolean>(false);
  const navigate = useNavigate(); // Initialize navigate

  const {user} = useUser()

  // Access the email address
const email = user && user.emailAddresses[0].emailAddress;

  useEffect(() => {
    let timeoutId: ReturnType<typeof setTimeout>;

    if (loading) {
      timeoutId = setTimeout(() => {
        setShowWaitMessage(true);
      }, 5000); // Show wait message if loading takes more than 30 seconds
    } else {
      setShowWaitMessage(false);
    }

    return () => {
      clearTimeout(timeoutId); // Clear timeout on component unmount or when loading state changes
    };
  }, [loading]);

  const handleQuestionSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetchDocumentQA(question, email || '');
      console.log(res)
      setResponse(res.answer);
    } catch (error) {
      toast.error((error as any)?.response?.data?.error)
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
          {loading ? (showWaitMessage ? 'We are generating answers, please wait...' : 'Loading...') : 'Ask Question'}
        </button>
      </div>

      {response && (
        <div className="response-container">
          <h3>Response:</h3>
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
