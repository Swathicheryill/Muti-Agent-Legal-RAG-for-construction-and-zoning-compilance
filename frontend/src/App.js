import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Dashboard from './pages/Dashboard';
import ConflictResolver from './pages/ConflictResolver';
import TimePredictor from './pages/TimePredictor';
import Verifier from './pages/Verifier';
import InspectorChat from './pages/InspectorChat';
import KnowledgeBase from './pages/KnowledgeBase';

function Navigation() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link';

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
      <div className="container-fluid">
        <Link className="navbar-brand fw-bold" to="/">
          <span className="text-primary">⚖️</span> LegalRAG
          <small className="text-muted ms-2 fs-7">Construction Compliance</small>
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link className={isActive('/')} to="/">Dashboard</Link>
            </li>
            <li className="nav-item">
              <Link className={isActive('/conflict')} to="/conflict">Conflict Resolver</Link>
            </li>
            <li className="nav-item">
              <Link className={isActive('/predict')} to="/predict">Time Predictor</Link>
            </li>
            <li className="nav-item">
              <Link className={isActive('/verify')} to="/verify">Verifier</Link>
            </li>
            <li className="nav-item">
              <Link className={isActive('/chat')} to="/chat">Inspector Chat</Link>
            </li>
            <li className="nav-item">
              <Link className={isActive('/knowledge')} to="/knowledge">Knowledge Base</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <Toaster position="top-right" />
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/conflict" element={<ConflictResolver />} />
            <Route path="/predict" element={<TimePredictor />} />
            <Route path="/verify" element={<Verifier />} />
            <Route path="/chat" element={<InspectorChat />} />
            <Route path="/knowledge" element={<KnowledgeBase />} />
          </Routes>
        </main>
        <footer className="footer bg-dark text-light py-3 mt-5">
          <div className="container text-center">
            <small>
              Multi-Agent Legal RAG System — Construction & Zoning Compliance
              <br />
              Covering: Bangalore • Chennai • Delhi • Mumbai • Hyderabad
              <br />
              <span className="text-muted">Powered by Groq LLM • ChromaDB • FastAPI • React</span>
            </small>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
