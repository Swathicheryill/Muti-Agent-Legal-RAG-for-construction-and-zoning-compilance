import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { resolveConflict } from '../services/api';

const ConflictResolver = () => {
  const [conflictDescription, setConflictDescription] = useState('');
  const [city, setCity] = useState('');
  const [category, setCategory] = useState('');
  const [projectType, setProjectType] = useState('');
  const [projectSize, setProjectSize] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const cities = ['Bangalore', 'Chennai', 'Delhi', 'Mumbai', 'Hyderabad'];
  const categories = [
    'Building Construction', 'Environment', 'Water', 'Air',
    'Road & Infrastructure', 'Housing', 'Industry', 'Area/Zoning'
  ];
  const buildingTypes = [
    'Residential - Individual House', 'Residential - Apartment Complex',
    'Commercial - Office', 'Commercial - Retail Mall',
    'Industrial - Manufacturing', 'Mixed Use'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!conflictDescription.trim()) {
      toast.error('Please describe the conflict');
      return;
    }

    setLoading(true);
    try {
      const projectDetails = {};
      if (projectType) projectDetails.building_type = projectType;
      if (projectSize) projectDetails.project_size = projectSize;

      const response = await resolveConflict(
        conflictDescription,
        city || null,
        category || null,
        Object.keys(projectDetails).length > 0 ? projectDetails : null
      );
      setResult(response);
      toast.success('Conflict analysis complete!');
    } catch (err) {
      toast.error('Failed to analyze conflict. Check if backend is running.');
      console.error(err);
    }
    setLoading(false);
  };

  const exampleConflicts = [
    "BBMP requires 5m front setback for residential buildings but Karnataka state rules allow 3m for plots under 300 sq.m. Which standard applies for my 200 sq.m residential plot in Koramangala, Bangalore?",
    "Delhi MCD building bye-laws allow G+4 construction without lift on 12m road, but fire safety rules mandate lift for buildings above 15m height. My proposed building is 16m on a 12m road.",
    "CRZ notification prohibits construction within 200m of HTL, but Chennai GCC allows reconstruction within existing CRZ-II built-up areas. Can I extend my existing building in Besant Nagar?",
  ];

  return (
    <div className="animate-fade">
      <div className="section-header">
        <h2>⚔️ Conflict Resolver</h2>
        <p className="text-muted">Objective 1 — Resolve contradictory legal requirements across jurisdictions</p>
      </div>

      <div className="row g-4">
        {/* Input Panel */}
        <div className="col-lg-5">
          <div className="card">
            <div className="card-header bg-danger bg-opacity-10 text-danger">
              <h5 className="mb-0">🔍 Describe the Conflict</h5>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label fw-semibold">Conflict Description *</label>
                  <textarea
                    className="form-control"
                    rows={5}
                    value={conflictDescription}
                    onChange={(e) => setConflictDescription(e.target.value)}
                    placeholder="Describe the jurisdictional conflict, contradictory requirements, or legal dilemma..."
                  />
                </div>

                <div className="row mb-3">
                  <div className="col-6">
                    <label className="form-label fw-semibold">City</label>
                    <select className="form-select" value={city} onChange={(e) => setCity(e.target.value)}>
                      <option value="">Any City</option>
                      {cities.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                  </div>
                  <div className="col-6">
                    <label className="form-label fw-semibold">Category</label>
                    <select className="form-select" value={category} onChange={(e) => setCategory(e.target.value)}>
                      <option value="">Any Category</option>
                      {categories.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                  </div>
                </div>

                <div className="row mb-3">
                  <div className="col-6">
                    <label className="form-label fw-semibold">Building Type</label>
                    <select className="form-select" value={projectType} onChange={(e) => setProjectType(e.target.value)}>
                      <option value="">Select</option>
                      {buildingTypes.map(b => <option key={b} value={b}>{b}</option>)}
                    </select>
                  </div>
                  <div className="col-6">
                    <label className="form-label fw-semibold">Project Size</label>
                    <select className="form-select" value={projectSize} onChange={(e) => setProjectSize(e.target.value)}>
                      <option value="">Select</option>
                      <option value="Small (< 500 sq.m)">Small (&lt; 500 sq.m)</option>
                      <option value="Medium (500-2000 sq.m)">Medium</option>
                      <option value="Large (2000-10000 sq.m)">Large</option>
                      <option value="Mega (> 10000 sq.m)">Mega</option>
                    </select>
                  </div>
                </div>

                <button type="submit" className="btn btn-danger w-100" disabled={loading}>
                  {loading ? (
                    <><span className="spinner-border spinner-border-sm me-2" />Analyzing Conflict...</>
                  ) : '🔍 Resolve Conflict'}
                </button>
              </form>

              {/* Example conflicts */}
              <div className="mt-4">
                <h6 className="text-muted">💡 Example Conflicts:</h6>
                {exampleConflicts.map((ex, i) => (
                  <div key={i} className="border rounded p-2 mb-2 small text-muted" style={{ cursor: 'pointer' }}
                    onClick={() => setConflictDescription(ex)}>
                    {ex.substring(0, 120)}...
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Results Panel */}
        <div className="col-lg-7">
          {loading && (
            <div className="card">
              <div className="card-body text-center py-5">
                <div className="loading-spinner">
                  <div className="spinner-border text-danger mb-3" />
                  <p>Analyzing jurisdictional conflict...</p>
                  <small className="text-muted">Retrieving relevant laws and applying resolution strategies</small>
                </div>
              </div>
            </div>
          )}

          {!loading && result && (
            <div className="animate-fade">
              {/* Summary Card */}
              {result.conflict_summary && (
                <div className="card mb-3">
                  <div className="card-header bg-danger bg-opacity-10 text-danger">
                    <h5 className="mb-0">📋 Conflict Summary</h5>
                  </div>
                  <div className="card-body">
                    <p>{result.conflict_summary}</p>
                    {result.jurisdictions_involved && (
                      <div className="d-flex flex-wrap gap-1 mt-2">
                        {result.jurisdictions_involved.map((j, i) => (
                          <span key={i} className="badge bg-secondary">{j}</span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Resolution */}
              {result.resolution && (
                <div className="card mb-3">
                  <div className="card-header bg-success bg-opacity-10 text-success">
                    <h5 className="mb-0">✅ Resolution</h5>
                  </div>
                  <div className="card-body">
                    <h6>Strategy: {result.resolution.strategy}</h6>
                    <p><strong>Recommended Action:</strong> {result.resolution.recommended_action}</p>
                    {result.resolution.compliant_value && (
                      <p><strong>Compliant Value:</strong> <code>{result.resolution.compliant_value}</code></p>
                    )}
                    {result.resolution.rationale && (
                      <div className="bg-light p-3 rounded mt-2">
                        <small className="text-muted">Rationale</small>
                        <p className="mb-0">{result.resolution.rationale}</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Legal Analysis */}
              {result.legal_analysis && (
                <div className="card mb-3">
                  <div className="card-header"><h5 className="mb-0">⚖️ Legal Analysis</h5></div>
                  <div className="card-body">
                    <p>{result.legal_analysis}</p>
                    {result.applicable_doctrines && (
                      <div className="mt-2">
                        <small className="text-muted">Applicable Doctrines:</small>
                        <div className="d-flex flex-wrap gap-1 mt-1">
                          {result.applicable_doctrines.map((d, i) => (
                            <span key={i} className="tag">{d}</span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Risk Assessment */}
              {result.risk_assessment && (
                <div className="card mb-3">
                  <div className="card-header"><h5 className="mb-0">⚠️ Risk Assessment</h5></div>
                  <div className="card-body">
                    <div className="d-flex align-items-center mb-2">
                      <span className="me-2">Risk Level:</span>
                      <span className={`finding-badge ${result.risk_assessment.level?.toLowerCase() || 'minor'}`}>
                        {result.risk_assessment.level}
                      </span>
                    </div>
                    {result.risk_assessment.potential_penalties && (
                      <p><strong>Penalties:</strong> {result.risk_assessment.potential_penalties}</p>
                    )}
                    {result.risk_assessment.mitigation_steps && (
                      <ul className="list-unstyled">
                        {result.risk_assessment.mitigation_steps.map((step, i) => (
                          <li key={i} className="mb-1">• {step}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              )}

              {/* Confidence Score */}
              {result.confidence_score && (
                <div className="card mb-3">
                  <div className="card-body d-flex align-items-center">
                    <span className="me-3 fw-semibold">Confidence Score:</span>
                    <div className="progress flex-grow-1" style={{ height: '24px' }}>
                      <div
                        className={`progress-bar ${result.confidence_score > 0.7 ? 'bg-success' : result.confidence_score > 0.4 ? 'bg-warning' : 'bg-danger'}`}
                        style={{ width: `${result.confidence_score * 100}%` }}
                      >
                        {(result.confidence_score * 100).toFixed(0)}%
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Raw JSON */}
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">📄 Full Response (JSON)</h5>
                </div>
                <div className="card-body">
                  <pre className="bg-dark text-light p-3 rounded" style={{ maxHeight: '400px', overflow: 'auto', fontSize: '0.8rem' }}>
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          )}

          {!loading && !result && (
            <div className="card">
              <div className="card-body text-center py-5 text-muted">
                <span className="fs-1">⚔️</span>
                <h5 className="mt-3">Describe a Legal Conflict</h5>
                <p>Enter a conflict description and the AI will analyze applicable laws across jurisdictions and recommend a resolution.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ConflictResolver;
