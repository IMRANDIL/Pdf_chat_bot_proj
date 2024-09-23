import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { fetchDocumentQA, listDocuments } from '../../services/api'; // Import the new API method
import { toast } from 'react-toastify';
import { useUser } from '@clerk/clerk-react';

const DocumentQAForm: React.FC = () => {
  const [question, setQuestion] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [showWaitMessage, setShowWaitMessage] = useState<boolean>(false);
  const [documents, setDocuments] = useState<string[]>([]);
  const [selectedDocument, setSelectedDocument] = useState<string>(''); // State for selected document
  const navigate = useNavigate(); // Initialize navigate

  const { user } = useUser();

  // Access the email address
  const email = user && user.emailAddresses[0].emailAddress;

  useEffect(() => {
    const fetchDocuments = async () => {
      if (email) {
        try {
          const docList = await listDocuments(email);
          setDocuments(docList.documents);
        } catch (error) {
          toast.error('Failed to fetch documents');
          console.error('Error fetching documents:', error);
        }
      }
    };

    fetchDocuments();
  }, [email]);

  useEffect(() => {
    let timeoutId: ReturnType<typeof setTimeout>;

    if (loading) {
      timeoutId = setTimeout(() => {
        setShowWaitMessage(true);
      }, 5000); // Show wait message if loading takes more than 5 seconds
    } else {
      setShowWaitMessage(false);
    }

    return () => {
      clearTimeout(timeoutId); // Clear timeout on component unmount or when loading state changes
    };
  }, [loading]);

  const handleQuestionSubmit = async () => {
    if (!selectedDocument) {
      toast.error('Please select a document before asking a question.');
      return;
    }

    setLoading(true);
    try {
      const res = await fetchDocumentQA(question, email || '', selectedDocument || '');
      setResponse(res.answer);
    } catch (error) {
      toast.error((error as any)?.response?.data?.error);
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

      {/* Dropdown for selecting document */}
      <div className="input-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '10px 0' }}>
        <select 
          value={selectedDocument} 
          onChange={(e) => setSelectedDocument(e.target.value)}
          style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc', width: '100%', maxWidth: '300px' }}
        >
          <option value="">Select a Document</option>
          {documents && documents.map((doc, index) => (
            <option key={index} value={doc} style={{ fontFamily: 'Arial, sans-serif', fontSize: '14px' }}>{doc}</option>
          ))}
        </select>
      </div>

      <div className="input-container">
        <input
          type="text"
          placeholder="Enter your question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={handleQuestionSubmit} disabled={loading || !question || !selectedDocument}>
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
