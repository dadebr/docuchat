import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import CollectionsPage from './pages/CollectionsPage';
import ChatPage from './pages/ChatPage';
import HomePage from './pages/HomePage';
import './App.css';

function App() {
  const [activeCollection, setActiveCollection] = useState(null);

  return (
    <Router>
      <div className="App">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route 
              path="/collections" 
              element={
                <CollectionsPage 
                  onSelectCollection={setActiveCollection}
                />
              } 
            />
            <Route 
              path="/chat/:collectionId?" 
              element={
                <ChatPage 
                  activeCollection={activeCollection}
                />
              } 
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
