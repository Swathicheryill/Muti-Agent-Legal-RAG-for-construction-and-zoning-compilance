import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getStats } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const data = await getStats();
        setStats(data);
      } catch (e) {
        console.error('Failed to load stats:', e);
      }
    };
    loadStats();
  }, []);

  return (
    <div className="animate-fade">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="row align-items-center">
          <div className="col-lg-8">
            <h1>Multi-Agent Legal RAG</h1>
            <p className="mb-3">
              AI-powered construction & zoning compliance system for Indian metropolitan cities.
              Resolves cross-jurisdictional legal conflicts, predicts future violations,
              and generates inspector-ready compliance reports.
            </p>
            <div className="hero-badges">
              <span className="badge bg-light text-dark">⚖️ Conflict Resolution</span>
              <span className="badge bg-light text-dark">🔮 Time Prediction</span>
              <span className="badge bg-light text-dark">✅ Verification Reports</span>
              <span className="badge bg-light text-dark">🤖 Inspector Chatbot</span>
            </div>
          </div>
          <div className="col-lg-4 text-center mt-3">
            <div className="bg-white bg-opacity-10 rounded-4 p-3">
              <h4 className="mb-2">5 Indian Cities</h4>
              <div className="d-flex flex-wrap justify-content-center gap-1">
                {['Bangalore', 'Chennai', 'Delhi', 'Mumbai', 'Hyderabad'].map(city => (
                  <span key={city} className="badge bg-warning text-dark">{city}</span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row g-4 mb-4">
        <div className="col-md-6 col-lg-3">
          <div className="card stat-card conflict h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-start">
                <div>
                  <p className="text-muted mb-1 small">Knowledge Base</p>
                  <h3 className="mb-0">67+</h3>
                  <small className="text-muted">Laws & Regulations</small>
                </div>
                <span className="fs-2">📚</span>
              </div>
              <div className="mt-2">
                <span className="tag">Building</span>
                <span className="tag">Environment</span>
                <span className="tag">Water</span>
                <span className="tag">Air</span>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6 col-lg-3">
          <div className="card stat-card predict h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-start">
                <div>
                  <p className="text-muted mb-1 small">Training Data</p>
                  <h3 className="mb-0">14,000+</h3>
                  <small className="text-muted">Synthetic Scenarios</small>
                </div>
                <span className="fs-2">📊</span>
              </div>
              <div className="mt-2">
                <span className="tag">5,500 Conflicts</span>
                <span className="tag">5,000 Predictions</span>
                <span className="tag">3,500 Reports</span>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6 col-lg-3">
          <div className="card stat-card verify h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-start">
                <div>
                  <p className="text-muted mb-1 small">AI Agents</p>
                  <h3 className="mb-0">5</h3>
                  <small className="text-muted">Specialized Agents</small>
                </div>
                <span className="fs-2">🤖</span>
              </div>
              <div className="mt-2">
                <span className="tag">Conflict Resolver</span>
                <span className="tag">Time Predictor</span>
                <span className="tag">Verifier</span>
                <span className="tag">Chatbot</span>
              </div>
            </div>
          </div>
        </div>

        <div className="card stat-card chat h-100 col-md-6 col-lg-3">
          <div className="card-body">
            <div className="d-flex justify-content-between align-items-start">
              <div>
                <p className="text-muted mb-1 small">Coverage</p>
                <h3 className="mb-0">7</h3>
                <small className="text-muted">Law Categories</small>
              </div>
              <span className="fs-2">🏛️</span>
            </div>
            <div className="mt-2">
              <span className="tag">Housing</span>
              <span className="tag">Road</span>
              <span className="tag">Industry</span>
              <span className="tag">Zoning</span>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="row g-4 mb-4">
        <div className="col-lg-4">
          <Link to="/conflict" className="text-decoration-none">
            <div className="card h-100 border-danger">
              <div className="card-body">
                <div className="d-flex align-items-center mb-3">
                  <span className="fs-1 me-3">⚔️</span>
                  <div>
                    <h5 className="text-danger mb-0">Conflict Resolver</h5>
                    <small className="text-muted">Objective 1</small>
                  </div>
                </div>
                <p className="text-secondary">
                  Autonomously reconciles contradictory legal requirements across overlapping jurisdictions.
                  Compares local → state → federal laws and applies resolution strategies.
                </p>
                <div className="d-flex justify-content-between align-items-center">
                  <span className="badge bg-danger bg-opacity-10 text-danger">5,500+ scenarios</span>
                  <span className="text-danger fw-semibold">Try it →</span>
                </div>
              </div>
            </div>
          </Link>
        </div>

        <div className="col-lg-4">
          <Link to="/predict" className="text-decoration-none">
            <div className="card h-100 border-warning">
              <div className="card-body">
                <div className="d-flex align-items-center mb-3">
                  <span className="fs-1 me-3">🔮</span>
                  <div>
                    <h5 className="text-warning mb-0">Time Predictor</h5>
                    <small className="text-muted">Objective 2</small>
                  </div>
                </div>
                <p className="text-secondary">
                  Predicts future compliance violations 6-12 months ahead with probabilistic
                  compliance roadmaps and confidence intervals.
                </p>
                <div className="d-flex justify-content-between align-items-center">
                  <span className="badge bg-warning bg-opacity-10 text-warning">5,000+ scenarios</span>
                  <span className="text-warning fw-semibold">Try it →</span>
                </div>
              </div>
            </div>
          </Link>
        </div>

        <div className="col-lg-4">
          <Link to="/verify" className="text-decoration-none">
            <div className="card h-100 border-success">
              <div className="card-body">
                <div className="d-flex align-items-center mb-3">
                  <span className="fs-1 me-3">✅</span>
                  <div>
                    <h5 className="text-success mb-0">Verifier</h5>
                    <small className="text-muted">Objective 3</small>
                  </div>
                </div>
                <p className="text-secondary">
                  Produces inspector-ready, legally defensible compliance reports with
                  traceable reasoning chains and minimum-change recommendations.
                </p>
                <div className="d-flex justify-content-between align-items-center">
                  <span className="badge bg-success bg-opacity-10 text-success">3,500+ scenarios</span>
                  <span className="text-success fw-semibold">Try it →</span>
                </div>
              </div>
            </div>
          </Link>
        </div>
      </div>

      {/* Chat CTA */}
      <div className="card bg-dark text-white mb-4">
        <div className="card-body p-4">
          <div className="row align-items-center">
            <div className="col-md-8">
              <h4 className="mb-1">💬 Inspector Chat</h4>
              <p className="mb-0 text-white-50">
                Chat with AI-powered construction inspectors and authority persons.
                Choose from 4 expert personas: Municipal Engineer, Environmental Officer,
                Fire Safety Officer, or Legal Advisor.
              </p>
            </div>
            <div className="col-md-4 text-end">
              <Link to="/chat" className="btn btn-primary btn-lg">
                Start Chat →
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* How it Works */}
      <div className="card mb-4">
        <div className="card-header"><h5 className="mb-0">🏗️ How It Works</h5></div>
        <div className="card-body">
          <div className="row text-center">
            {[
              { icon: '📚', title: 'Knowledge Base', desc: '67+ Indian construction laws indexed in vector store' },
              { icon: '🔍', title: 'RAG Retrieval', desc: 'Relevant laws retrieved via semantic search' },
              { icon: '🤖', title: 'Multi-Agent AI', desc: '5 specialized agents analyze using Groq LLM' },
              { icon: '📋', title: 'Structured Output', desc: 'JSON reports with reasoning chains' },
            ].map((step, i) => (
              <div key={i} className="col-md-3">
                <div className="p-3">
                  <span className="fs-1">{step.icon}</span>
                  <h6 className="mt-2">{step.title}</h6>
                  <small className="text-muted">{step.desc}</small>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
