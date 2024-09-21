import React from 'react';
import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/clerk-react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import DocumentQAForm from './components/DocumentQA/DocumentQAForm';
import './App.css';
import gifyBot from './assets/giphy_bot.gif';

const App: React.FC = () => {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <header style={{ textAlign: 'center' }}>
        <SignedOut>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <img 
              src={gifyBot}
              alt="PDF Chat Bot" 
              style={{ width: '100%', maxWidth: '300px', marginBottom: '20px', borderRadius: '8px' }} 
            />
            <SignInButton style={{ padding: '10px 20px', fontSize: '18px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
              Sign In
            </SignInButton>
          </div>
        </SignedOut>
        <SignedIn>
          <UserButton />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/qa" element={<DocumentQAForm />} />
          </Routes>
        </SignedIn>
      </header>
    </div>
  );
};

export default App;
