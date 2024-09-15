import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import './App.css'
import DocumentQAForm from './components/DocumentQA/DocumentQAForm';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/qa" element={<DocumentQAForm />} />
      </Routes>
    </Router>
  );
};

export default App;
