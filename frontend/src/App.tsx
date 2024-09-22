import React from 'react';
import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/clerk-react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import DocumentQAForm from './components/DocumentQA/DocumentQAForm';
import './App.css';
import gifyBot from './assets/giphy_bot.gif';
import { useUser } from '@clerk/clerk-react'
import backgroundImage from './assets/black-white-background.jpg'



const App: React.FC = () => {
  const {user} = useUser()

  // Access the email address
const email = user && user.emailAddresses[0].emailAddress;
  return (
    <>
    {!email && <h2 style={{textAlign:'center'}}>Please Sign In to chat your doc(pdf)</h2>}
    <div style={{ display: 'flex', justifyContent: 'center', height: '100vh', backgroundImage: `url(${!email && backgroundImage})`, backgroundPosition: 'center', backgroundSize: 'cover' }}>
      <header style={{ textAlign: 'center' }}>
       
        <SignedOut>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <img 
              src={gifyBot}
              alt="PDF Chat Bot" 
              style={{ width: '100%', maxWidth: '200px', marginBottom: '20px', borderRadius: '8px', marginTop:'18px' }} 
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
    </>
  );
};

export default App;
