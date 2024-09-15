import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadPDF } from '../../services/api';

const UploaderForm: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF file to upload.');
      return;
    }

    try {
      const {status, data} = await uploadPDF(file);
      if (status == 200 && data.message) {
        // Redirect to DocumentQAForm screen after successful upload
        navigate('/qa');
      } else {
        setError('Error uploading file');
      }
    } catch (err) {
      console.error('Error uploading file:', err);
      setError('Error uploading file');
    }
  };

  return (
    <div className="uploader-form">
      <h2>Upload Your PDF</h2>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      {error && <p className="error-text">{error}</p>}
      <button onClick={handleUpload} disabled={!file}>Upload PDF</button>
    </div>
  );
};

export default UploaderForm;
