import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { searchKnowledgeBase } from '../services/api';

const KnowledgeBase = () => {
  const [query, setQuery] = useState('');
  const [city, setCity] = useState('');
  const [category, setCategory] = useState('');
  const [topK, setTopK] = useState(5);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const cities = ['Bangalore', 'Chennai', 'Delhi', 'Mumbai', 'Hyderabad'];
  const categories = [
    'Building Construction', 'Environment', 'Water', 'Air',
    'Road & Infrastructure', 'Housing', 'Industry', 'Area/Zoning'
  ];

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      toast.error('Please enter a search query');
      return;
    }

    setLoading(true);
    try {
      const data = await searchKnowledgeBase(query, city || null, category || null, topK);
      setResults(data);
      toast.success(`Found ${data.count} results`);
    } catch (err) {
      toast.error('Search failed. Make sure backend is running and KB is indexed.');
      console.error(err);
    }
    setLoading(false);
  };

  const exampleQueries = [
    "What is the FAR requirement for residential buildings in Bangalore?",
    "Fire safety requirements for buildings above 15 meters",
    "CRZ regulations for coastal construction in Chennai",
    "Rainwater harvesting mandatory requirements across Indian cities",
    "RERA registration requirements and penalties",
    "Environmental clearance for construction projects",
    "Parking requirements for commercial buildings",
    "Setback requirements for buildings near highways",
  ];

  const categoryIcons = {
    'Building Construction': '🏗️',
    'Environment': '🌿',
    'Water': '💧',
    'Air': '🌬️',
    'Road & Infrastructure': '🛣️',
    'Housing': '🏠',
    'Industry': '🏭',
    'Area/Zoning': '📐',
  };

  return (
    <div className="animate-fade">
      <div className="section-header">
        <h2>📚 Knowledge Base</h2>
        <p className="text-muted">Search 67+ Indian construction laws across 7 categories and 5 cities</p>
      </div>

      {/* Search Form */}
      <div className="card mb-4">
        <div className="card-body">
          <form onSubmit={handleSearch}>
            <div className="row g-3">
              <div className="col-lg-6">
                <label className="form-label fw-semibold">Search Query</label>
                <input
                  type="text"
                  className="form-control form-control-lg"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search laws, regulations, requirements..."
                />
              </div>
              <div className="col-lg-2">
                <label className="form-label fw-semibold">City</label>
                <select className="form-select" value={city} onChange={(e) => setCity(e.target.value)}>
                  <option value="">All Cities</option>
                  {cities.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div className="col-lg-2">
                <label className="form-label fw-semibold">Category</label>
                <select className="form-select" value={category} onChange={(e) => setCategory(e.target.value)}>
                  <option value="">All Categories</option>
                  {categories.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div className="col-lg-2 d-flex align-items-end">
                <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                  {loading ? <span className="spinner-border spinner-border-sm" /> : '🔍 Search'}
                </button>
              </div>
            </div>
          </form>

          {/* Example queries */}
          <div className="mt-3">
            <small className="text-muted me-2">Try:</small>
            {exampleQueries.slice(0, 4).map((q, i) => (
              <button key={i} className="btn btn-sm btn-outline-secondary me-1 mb-1"
                onClick={() => setQuery(q)}>
                {q.substring(0, 40)}...
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      {results && results.results && results.results.length > 0 && (
        <div className="animate-fade">
          <h5 className="mb-3">Results ({results.count} found)</h5>
          {results.results.map((r, i) => (
            <div key={i} className="card mb-3">
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <span className="badge bg-primary me-2">
                      {categoryIcons[r.metadata?.category] || '📄'} {r.metadata?.category}
                    </span>
                    <span className="badge bg-secondary me-2">{r.metadata?.city || 'All'}</span>
                    <span className="badge bg-info">{r.metadata?.state}</span>
                  </div>
                  <span className="badge bg-success">
                    Relevance: {(r.relevance_score * 100).toFixed(0)}%
                  </span>
                </div>
                <h6 className="mb-1">{r.metadata?.law_name}</h6>
                <p className="mb-1 small text-muted">
                  Authority: {r.metadata?.authority} | Subcategory: {r.metadata?.subcategory}
                </p>
                <div className="bg-light p-3 rounded mt-2">
                  <p className="mb-0 small" style={{ whiteSpace: 'pre-wrap' }}>{r.text}</p>
                </div>
                {r.metadata?.tags && (
                  <div className="mt-2 d-flex flex-wrap gap-1">
                    {r.metadata.tags.split(',').filter(Boolean).map((tag, j) => (
                      <span key={j} className="tag">{tag.trim()}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {results && results.count === 0 && (
        <div className="card">
          <div className="card-body text-center py-5 text-muted">
            <span className="fs-1">🔍</span>
            <h5 className="mt-3">No Results Found</h5>
            <p>Try a different search query or broaden your filters.</p>
          </div>
        </div>
      )}

      {/* Category Overview */}
      {!results && (
        <div className="row g-3">
          {categories.map(cat => (
            <div key={cat} className="col-md-4">
              <div className="card h-100" style={{ cursor: 'pointer' }}
                onClick={() => { setCategory(cat); }}>
                <div className="card-body text-center">
                  <span className="fs-1">{categoryIcons[cat]}</span>
                  <h6 className="mt-2">{cat}</h6>
                  <small className="text-muted">Click to filter</small>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default KnowledgeBase;
