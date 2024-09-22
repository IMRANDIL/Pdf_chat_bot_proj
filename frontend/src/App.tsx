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
              style={{ width: '100%', maxWidth: '200px', marginBottom: '20px', borderRadius: '8px' }} 
            />
            <SignInButton>
            <button style={{ backgroundColor: '#007bff', color: 'white', padding: '10px 16px', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '16px' }}>Sign in</button>
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
