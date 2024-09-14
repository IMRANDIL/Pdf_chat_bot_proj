import React, { useState } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';
import { fetchDocumentQA } from '../../services/api';

const DocumentQAForm: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = await fetchDocumentQA(question);
    setResponse(data.answer);
  };

  return (
    <div className="qa-form">
      <form onSubmit={handleSubmit}>
        <Input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
          className="input-field"
        />
        <Button label="Submit" type="submit" className="submit-btn" onClick={() => {}} />
      </form>

      {response && (
        <div className="response">
          <h2>Answer:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default DocumentQAForm;
