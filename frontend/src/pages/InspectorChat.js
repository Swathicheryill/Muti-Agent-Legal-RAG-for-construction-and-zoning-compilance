import React, { useState, useRef, useEffect } from 'react';
import toast from 'react-hot-toast';
import { chatWithInspector, getPersonas } from '../services/api';

const InspectorChat = () => {
  const [messages, setMessages] = useState([
    {
      role: 'inspector',
      content: "Hello! I'm your AI construction compliance inspector. I can help you with building regulations, compliance requirements, and answer questions about construction laws in Indian cities.\n\nPlease select my expertise area below, or just start asking questions!",
      persona: 'System',
      avatar: '🤖',
    }
  ]);
  const [input, setInput] = useState('');
  const [persona, setPersona] = useState('municipal_engineer');
  const [personas, setPersonas] = useState({});
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    const loadPersonas = async () => {
      try {
        const data = await getPersonas();
        setPersonas(data);
      } catch (e) {
        // Use defaults
        setPersonas({
          municipal_engineer: { name: 'Er. Rajesh Kumar, Chief Municipal Engineer', role: 'Chief Municipal Engineer', avatar: '👨‍🔧' },
          environment_officer: { name: 'Dr. Priya Sharma, Environmental Officer', role: 'Environmental Compliance Officer', avatar: '👩‍🔬' },
          fire_safety_officer: { name: 'Capt. Vikram Singh, Fire Safety Officer', role: 'Fire Safety Officer', avatar: '🧑‍🚒' },
          legal_advisor: { name: 'Adv. Lakshmi Iyer, Legal Advisor', role: 'Construction Law Advisor', avatar: '👩‍⚖️' },
        });
      }
    };
    loadPersonas();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = { role: 'user', content: input, persona: 'You' };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const history = messages.slice(-10).map(m => ({
        role: m.role === 'user' ? 'user' : 'assistant',
        content: m.content,
      }));

      const response = await chatWithInspector(input, persona, history);
      const inspectorMsg = {
        role: 'inspector',
        content: response.response,
        persona: response.persona,
        avatar: response.avatar,
      };
      setMessages(prev => [...prev, inspectorMsg]);
    } catch (err) {
      toast.error('Failed to get response. Check if backend is running.');
      setMessages(prev => [...prev, {
        role: 'inspector',
        content: 'I apologize, but I encountered an error. Please try again.',
        persona: 'System',
        avatar: '⚠️',
      }]);
    }
    setLoading(false);
  };

  const handlePersonaChange = (newPersona) => {
    setPersona(newPersona);
    const p = personas[newPersona];
    if (p) {
      setMessages(prev => [...prev, {
        role: 'inspector',
        content: `I've switched to **${p.name}** (${p.role}). How can I assist you?`,
        persona: p.name,
        avatar: p.avatar,
      }]);
    }
  };

  const quickQuestions = [
    "What are the setback requirements for a G+4 building in Bangalore?",
    "Do I need environmental clearance for a 5000 sq.m commercial project?",
    "What is the parking requirement for a residential apartment complex?",
    "What fire safety measures are required for buildings above 15m?",
    "Is rainwater harvesting mandatory for my building?",
    "What is RERA and do I need to register?",
  ];

  return (
    <div className="animate-fade">
      <div className="section-header">
        <h2>💬 Inspector Chat</h2>
        <p className="text-muted">Chat with AI-powered construction inspectors and authority persons</p>
      </div>

      <div className="row g-4">
        {/* Persona Selector Sidebar */}
        <div className="col-lg-3">
          <div className="card mb-3">
            <div className="card-header bg-purple bg-opacity-10" style={{ background: '#f3e8ff' }}>
              <h6 className="mb-0">🧑‍💼 Select Persona</h6>
            </div>
            <div className="card-body p-2">
              {Object.entries(personas).map(([key, p]) => (
                <div key={key}
                  className={`persona-card p-2 rounded mb-2 ${persona === key ? 'selected' : ''}`}
                  onClick={() => handlePersonaChange(key)}>
                  <div className="d-flex align-items-center">
                    <span className="fs-3 me-2">{p.avatar}</span>
                    <div>
                      <small className="fw-bold d-block">{p.name}</small>
                      <small className="text-muted">{p.role}</small>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Questions */}
          <div className="card">
            <div className="card-header"><h6 className="mb-0">⚡ Quick Questions</h6></div>
            <div className="card-body p-2">
              {quickQuestions.map((q, i) => (
                <div key={i} className="border rounded p-2 mb-1 small" style={{ cursor: 'pointer' }}
                  onClick={() => setInput(q)}>
                  {q}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Chat Area */}
        <div className="col-lg-9">
          <div className="card">
            <div className="card-header d-flex justify-content-between align-items-center">
              <h6 className="mb-0">
                {personas[persona]?.avatar || '🤖'} {personas[persona]?.name || 'Inspector'}
              </h6>
              <span className="badge bg-success">Online</span>
            </div>

            {/* Messages */}
            <div className="chat-container" style={{ minHeight: '500px', maxHeight: '500px' }}>
              {messages.map((msg, i) => (
                <div key={i} className={`chat-message ${msg.role}`}>
                  {msg.role === 'inspector' && (
                    <div className="meta">
                      <span>{msg.avatar} {msg.persona}</span>
                    </div>
                  )}
                  {msg.role === 'user' && (
                    <div className="meta text-end">
                      <span>You</span>
                    </div>
                  )}
                  <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                </div>
              ))}
              {loading && (
                <div className="chat-message inspector">
                  <div className="meta">
                    <span>{personas[persona]?.avatar || '🤖'} {personas[persona]?.name}</span>
                  </div>
                  <div className="d-flex align-items-center">
                    <span className="spinner-border spinner-border-sm me-2" />
                    <span className="text-muted">Thinking...</span>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            {/* Input */}
            <div className="chat-input-area">
              <form onSubmit={handleSend}>
                <div className="input-group">
                  <input
                    type="text"
                    className="form-control"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about construction compliance..."
                    disabled={loading}
                  />
                  <button type="submit" className="btn btn-primary" disabled={loading || !input.trim()}>
                    {loading ? <span className="spinner-border spinner-border-sm" /> : 'Send'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InspectorChat;
