import React from 'react';
import UploaderForm from '../components/DocumentQA/UploaderForm';

const Home: React.FC = () => {
  return (
    <div className="home-container">
      <div className="home-content">
        <h1 className="home-title" style={{ textAlign: 'center' }}>Document Q&A</h1>
        <p className="home-description" style={{ textAlign: 'center', color:'black', background:'white', padding:'10px 20px', borderRadius:'10px' }}>
          Upload your document and ask any question to get accurate responses based on its content.
        </p>
        <UploaderForm />
      </div>
    </div>
  );
};

export default Home;
