import React from 'react';
import DocumentQAForm from '../components/DocumentQA/DocumentQAForm';


const Home: React.FC = () => {
  return (
    <div className="home-container">
      <div className="home-content">
        <h1 className="home-title">Document Q&A</h1>
        <p className="home-description">
          Ask any question about the documents and get accurate responses based on their content.
        </p>
        <DocumentQAForm />
      </div>
    </div>
  );
};

export default Home;
