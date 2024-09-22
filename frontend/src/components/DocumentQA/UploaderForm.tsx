import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadPDF } from '../../services/api';
import { useUser } from '@clerk/clerk-react'

const UploaderForm: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadText, setUploadText] = useState('Uploading...');
  const navigate = useNavigate();
  const {user} = useUser()

  // Access the email address
const email = user && user.emailAddresses[0].emailAddress;
  // Handle file change event
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  // Simulate upload state changes
  useEffect(() => {
    let timer:ReturnType<typeof setTimeout>;
    if (isUploading) {
      // Show "Please wait, still uploading..." after 10 seconds
      timer = setTimeout(() => {
        setUploadText('Please wait, still uploading...');
      }, 10000); // 10 seconds
    }
    return () => clearTimeout(timer);
  }, [isUploading]);

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF file to upload.');
      return;
    }

    setIsUploading(true); // Start showing loader
    setError(null); // Clear any previous error
    setUploadText('Uploading...');

    try {
      const { status, data } = await uploadPDF(file, email || '');
      if (status === 200 && data.message) {
        // Redirect to DocumentQAForm screen after successful upload
        navigate('/qa');
      } else {
        setError('Error uploading file');
      }
    } catch (err) {
      console.error('Error uploading file:', err);
      setError('Error uploading file');
    } finally {
      setIsUploading(false); // Stop showing loader
    }
  };

  return (
    <div className="uploader-form">
      <h2>Upload Your PDF</h2>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      {error && <p className="error-text">{error}</p>}
      
      {/* Show upload button or loader depending on upload state */}
      {isUploading ? (
        <div>
          <p>{uploadText}</p>
          <div className="loader" style={{ margin: '10px 0' }}></div> {/* Replace with your loader design */}
        </div>
      ) : (
        <button onClick={handleUpload} disabled={!file}>
          Upload PDF
        </button>
      )}
    </div>
  );
};

export default UploaderForm;
