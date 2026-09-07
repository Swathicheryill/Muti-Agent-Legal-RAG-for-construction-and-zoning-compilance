import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { predictCompliance } from '../services/api';

const TimePredictor = () => {
  const [description, setDescription] = useState('');
  const [city, setCity] = useState('');
  const [startDate, setStartDate] = useState('');
  const [duration, setDuration] = useState('');
  const [permits, setPermits] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const cities = ['Bangalore', 'Chennai', 'Delhi', 'Mumbai', 'Hyderabad'];
  const allPermits = [
    'Land Use Approval', 'Building Plan Approval', 'Environmental Clearance',
    'Fire NOC', 'Water Connection', 'Sewerage Connection', 'Power Connection',
    'RERA Registration', 'CTE/CTO'
  ];

  const togglePermit = (permit) => {
    setPermits(prev => prev.includes(permit) ? prev.filter(p => p !== permit) : [...prev, permit]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description.trim()) {
      toast.error('Please describe the project');
      return;
    }

    setLoading(true);
    try {
      const timeline = {};
      if (startDate) timeline.start_date = startDate;
      if (duration) timeline.duration_months = parseInt(duration);

      const response = await predictCompliance(
        description,
        city || null,
        Object.keys(timeline).length > 0 ? timeline : null,
        permits.length > 0 ? permits : null
      );
      setResult(response);
      toast.success('Prediction complete!');
    } catch (err) {
      toast.error('Failed to generate prediction.');
      console.error(err);
    }
    setLoading(false);
  };

  const examples = [
    "12-story residential apartment complex (200 units) on a 2-acre plot in Whitefield, Bangalore. Currently in foundation stage. Obtained building plan approval and RERA registration.",
    "Mixed-use commercial-retail building in Andheri, Mumbai. 8 floors with 3 levels of basement parking. Environmental clearance pending. Near the new metro line.",
    "IT park campus in Gachibowli, Hyderabad. 4 buildings of G+5 each. Total area 50,000 sq.m. All major permits obtained. Construction at structural stage.",
  ];

  return (
    <div className="animate-fade">
      <div className="section-header">
        <h2>🔮 Time Predictor</h2>
        <p className="text-muted">Objective 2 — Predict future compliance violations 6-12 months ahead</p>
      </div>

      <div className="row g-4">
        <div className="col-lg-5">
          <div className="card">
            <div className="card-header bg-warning bg-opacity-10 text-warning">
              <h5 className="mb-0">📊 Project Details</h5>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label fw-semibold">Project Description *</label>
                  <textarea
                    className="form-control"
                    rows={4}
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Describe your construction project in detail..."
                  />
                </div>

                <div className="row mb-3">
                  <div className="col-6">
                    <label className="form-label fw-semibold">City</label>
                    <select className="form-select" value={city} onChange={(e) => setCity(e.target.value)}>
                      <option value="">Select City</option>
                      {cities.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                  </div>
                  <div className="col-6">
                    <label className="form-label fw-semibold">Duration (months)</label>
                    <input type="number" className="form-control" value={duration}
                      onChange={(e) => setDuration(e.target.value)} placeholder="e.g., 24" />
                  </div>
                </div>

                <div className="mb-3">
                  <label className="form-label fw-semibold">Start Date</label>
                  <input type="date" className="form-control" value={startDate}
                    onChange={(e) => setStartDate(e.target.value)} />
                </div>

                <div className="mb-3">
                  <label className="form-label fw-semibold">Current Permits Obtained</label>
                  <div className="d-flex flex-wrap gap-1">
                    {allPermits.map(permit => (
                      <button key={permit} type="button"
                        className={`btn btn-sm ${permits.includes(permit) ? 'btn-primary' : 'btn-outline-secondary'}`}
                        onClick={() => togglePermit(permit)}>
                        {permit}
                      </button>
                    ))}
                  </div>
                </div>

                <button type="submit" className="btn btn-warning w-100 fw-semibold" disabled={loading}>
                  {loading ? (
                    <><span className="spinner-border spinner-border-sm me-2" />Predicting...</>
                  ) : '🔮 Predict Future Risks'}
                </button>
              </form>

              <div className="mt-4">
                <h6 className="text-muted">💡 Example Projects:</h6>
                {examples.map((ex, i) => (
                  <div key={i} className="border rounded p-2 mb-2 small text-muted" style={{ cursor: 'pointer' }}
                    onClick={() => setDescription(ex)}>
                    {ex.substring(0, 100)}...
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-7">
          {loading && (
            <div className="card">
              <div className="card-body text-center py-5">
                <div className="loading-spinner">
                  <div className="spinner-border text-warning mb-3" />
                  <p>Analyzing project timeline and regulatory trends...</p>
                  <small className="text-muted">This may take a moment for complex analysis</small>
                </div>
              </div>
            </div>
          )}

          {!loading && result && (
            <div className="animate-fade">
              {/* Predictions */}
              {result.predictions && result.predictions.length > 0 && (
                <div className="card mb-3">
                  <div className="card-header bg-warning bg-opacity-10">
                    <h5 className="mb-0">🔮 Predicted Regulatory Changes</h5>
                  </div>
                  <div className="card-body">
                    {result.predictions.map((pred, i) => (
                      <div key={i} className="border rounded p-3 mb-3">
                        <div className="d-flex justify-content-between align-items-start">
                          <div>
                            <h6 className="mb-1">{pred.change_type}</h6>
                            <p className="mb-1 small">{pred.description}</p>
                          </div>
                          <span className={`badge ${pred.confidence > 0.7 ? 'bg-danger' : pred.confidence > 0.4 ? 'bg-warning' : 'bg-secondary'}`}>
                            {(pred.confidence * 100).toFixed(0)}% confidence
                          </span>
                        </div>
                        <div className="d-flex align-items-center mt-2">
                          <small className="text-muted me-2">Timeline:</small>
                          <span className="badge bg-info">{pred.predicted_timeframe_months} months</span>
                          {pred.confidence_interval && (
                            <small className="text-muted ms-2">
                              CI: [{(pred.confidence_interval.lower * 100).toFixed(0)}% - {(pred.confidence_interval.upper * 100).toFixed(0)}%]
                            </small>
                          )}
                        </div>
                        {pred.key_indicators && (
                          <div className="mt-2 d-flex flex-wrap gap-1">
                            {pred.key_indicators.map((ind, j) => (
                              <span key={j} className="tag">{ind}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Compliance Roadmap */}
              {result.compliance_roadmap && (
                <div className="card mb-3">
                  <div className="card-header"><h5 className="mb-0">🗺️ Compliance Roadmap</h5></div>
                  <div className="card-body">
                    {result.compliance_roadmap.overall_risk_level && (
                      <div className="d-flex align-items-center mb-3">
                        <span className="me-2 fw-semibold">Overall Risk:</span>
                        <span className={`finding-badge ${result.compliance_roadmap.overall_risk_level.toLowerCase()}`}>
                          {result.compliance_roadmap.overall_risk_level}
                        </span>
                        {result.compliance_roadmap.overall_risk_score && (
                          <span className="ms-2 text-muted">
                            ({(result.compliance_roadmap.overall_risk_score * 100).toFixed(0)}%)
                          </span>
                        )}
                      </div>
                    )}

                    {result.compliance_roadmap.milestones && result.compliance_roadmap.milestones.map((m, i) => (
                      <div key={i} className="timeline-item mb-3">
                        <div className="d-flex justify-content-between">
                          <h6 className="mb-1">{m.milestone}</h6>
                          <span className="badge bg-secondary">{m.timeline_months} months</span>
                        </div>
                        <p className="mb-1 small">{m.action_required}</p>
                        {m.estimated_cost_impact && (
                          <small className="text-muted">Cost Impact: {m.estimated_cost_impact}</small>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Recommendations */}
              {result.proactive_recommendations && (
                <div className="card mb-3">
                  <div className="card-header"><h5 className="mb-0">💡 Proactive Recommendations</h5></div>
                  <div className="card-body">
                    {result.proactive_recommendations.map((rec, i) => (
                      <div key={i} className="d-flex align-items-start mb-2">
                        <span className={`badge me-2 ${rec.priority === 'High' ? 'bg-danger' : rec.priority === 'Medium' ? 'bg-warning' : 'bg-secondary'}`}>
                          {rec.priority}
                        </span>
                        <div>
                          <p className="mb-0">{rec.action}</p>
                          <small className="text-muted">Timeline: {rec.timeline}</small>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Confidence */}
              {result.confidence_score && (
                <div className="card mb-3">
                  <div className="card-body d-flex align-items-center">
                    <span className="me-3 fw-semibold">Prediction Confidence:</span>
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
                <span className="fs-1">🔮</span>
                <h5 className="mt-3">Predict Compliance Risks</h5>
                <p>Enter project details to get AI-powered predictions of future regulatory changes and compliance risks.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TimePredictor;
