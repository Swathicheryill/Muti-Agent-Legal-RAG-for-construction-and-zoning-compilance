import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { verifyCompliance } from '../services/api';

const Verifier = () => {
  const [description, setDescription] = useState('');
  const [city, setCity] = useState('');
  const [category, setCategory] = useState('');
  const [scope, setScope] = useState('full');
  const [inspectorName, setInspectorName] = useState('');
  const [inspectorType, setInspectorType] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const cities = ['Bangalore', 'Chennai', 'Delhi', 'Mumbai', 'Hyderabad'];
  const categories = [
    'Building Construction', 'Environment', 'Water', 'Air',
    'Road & Infrastructure', 'Housing', 'Industry'
  ];
  const scopes = [
    { value: 'full', label: 'Full Compliance Check' },
    { value: 'structural', label: 'Structural Safety Only' },
    { value: 'fire', label: 'Fire Safety Only' },
    { value: 'environmental', label: 'Environmental Only' },
    { value: 'accessibility', label: 'Accessibility Audit' },
  ];
  const inspectorTypes = [
    'Chief Engineer', 'Structural Engineer', 'Environmental Officer',
    'Fire Safety Officer', 'Municipal Engineer'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description.trim()) {
      toast.error('Please describe the project');
      return;
    }

    setLoading(true);
    try {
      const inspectionDetails = {};
      if (inspectorName) inspectionDetails.inspector_name = inspectorName;
      if (inspectorType) inspectionDetails.inspector_designation = inspectorType;

      const response = await verifyCompliance(
        description,
        city || null,
        category || null,
        scope
      );
      setResult(response);
      toast.success('Verification report generated!');
    } catch (err) {
      toast.error('Failed to generate report.');
      console.error(err);
    }
    setLoading(false);
  };

  const examples = [
    "20-story residential tower in Koramangala, Bangalore. G+19, 4 units per floor. Completed construction. Seeking Occupancy Certificate. Has building plan approval, fire NOC, and structural stability certificate.",
    "New commercial office building in Noida, Delhi NCR. G+8 with 2 basement levels. Under construction at 4th floor. Environmental clearance and building plan obtained.",
    "Residential complex in Porur, Chennai. 3 towers of G+12 each, 200 units total. Completed construction. STP and RWH installed. Seeking OC.",
  ];

  return (
    <div className="animate-fade">
      <div className="section-header">
        <h2>✅ Compliance Verifier</h2>
        <p className="text-muted">Objective 3 — Generate inspector-ready compliance reports</p>
      </div>

      <div className="row g-4">
        <div className="col-lg-5">
          <div className="card">
            <div className="card-header bg-success bg-opacity-10 text-success">
              <h5 className="mb-0">📋 Project Details</h5>
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
                    placeholder="Describe the project for compliance verification..."
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
                    <label className="form-label fw-semibold">Scope</label>
                    <select className="form-select" value={scope} onChange={(e) => setScope(e.target.value)}>
                      {scopes.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
                    </select>
                  </div>
                </div>

                <div className="mb-3">
                  <label className="form-label fw-semibold">Category Focus</label>
                  <select className="form-select" value={category} onChange={(e) => setCategory(e.target.value)}>
                    <option value="">All Categories</option>
                    {categories.map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>

                <div className="row mb-3">
                  <div className="col-6">
                    <label className="form-label fw-semibold">Inspector Name</label>
                    <input type="text" className="form-control" value={inspectorName}
                      onChange={(e) => setInspectorName(e.target.value)} placeholder="Er. Name" />
                  </div>
                  <div className="col-6">
                    <label className="form-label fw-semibold">Inspector Type</label>
                    <select className="form-select" value={inspectorType} onChange={(e) => setInspectorType(e.target.value)}>
                      <option value="">Select</option>
                      {inspectorTypes.map(t => <option key={t} value={t}>{t}</option>)}
                    </select>
                  </div>
                </div>

                <button type="submit" className="btn btn-success w-100 fw-semibold" disabled={loading}>
                  {loading ? (
                    <><span className="spinner-border spinner-border-sm me-2" />Generating Report...</>
                  ) : '✅ Generate Report'}
                </button>
              </form>

              <div className="mt-4">
                <h6 className="text-muted">💡 Example Projects:</h6>
                {examples.map((ex, i) => (
                  <div key={i} className="border rounded p-2 mb-2 small text-muted" style={{ cursor: 'pointer' }}
                    onClick={() => setDescription(ex)}>
                    {ex.substring(0, 120)}...
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
                  <div className="spinner-border text-success mb-3" />
                  <p>Generating compliance report...</p>
                  <small className="text-muted">Checking all applicable regulations</small>
                </div>
              </div>
            </div>
          )}

          {!loading && result && (
            <div className="animate-fade">
              {/* Report Metadata */}
              {result.report_metadata && (
                <div className="card mb-3">
                  <div className="card-header bg-success bg-opacity-10 text-success">
                    <h5 className="mb-0">📋 Report: {result.report_metadata.report_type}</h5>
                  </div>
                  <div className="card-body">
                    <div className="row">
                      <div className="col-4"><small className="text-muted">Report ID</small><br /><strong>{result.report_metadata.report_id}</strong></div>
                      <div className="col-4"><small className="text-muted">Generated</small><br /><strong>{result.report_metadata.generated_date}</strong></div>
                      <div className="col-4"><small className="text-muted">Authority</small><br /><strong>{result.report_metadata.reporting_authority}</strong></div>
                    </div>
                  </div>
                </div>
              )}

              {/* Compliance Summary */}
              {result.compliance_summary && (
                <div className="card mb-3">
                  <div className="card-header"><h5 className="mb-0">📊 Compliance Summary</h5></div>
                  <div className="card-body">
                    <div className="row text-center mb-3">
                      <div className="col">
                        <div className="border rounded p-2">
                          <h4 className="text-danger mb-0">{result.compliance_summary.critical_findings || 0}</h4>
                          <small>Critical</small>
                        </div>
                      </div>
                      <div className="col">
                        <div className="border rounded p-2">
                          <h4 className="text-warning mb-0">{result.compliance_summary.major_findings || 0}</h4>
                          <small>Major</small>
                        </div>
                      </div>
                      <div className="col">
                        <div className="border rounded p-2">
                          <h4 className="text-info mb-0">{result.compliance_summary.minor_findings || 0}</h4>
                          <small>Minor</small>
                        </div>
                      </div>
                      <div className="col">
                        <div className="border rounded p-2">
                          <h4 className="text-success mb-0">{result.compliance_summary.compliant_items || 0}</h4>
                          <small>Compliant</small>
                        </div>
                      </div>
                    </div>

                    {result.compliance_summary.overall_status && (
                      <div className="d-flex align-items-center justify-content-center">
                        <span className="me-2">Overall Status:</span>
                        <span className={`finding-badge ${result.compliance_summary.overall_status.includes('Non') ? 'critical' : result.compliance_summary.overall_status.includes('Partial') ? 'major' : 'compliant'}`}>
                          {result.compliance_summary.overall_status}
                        </span>
                      </div>
                    )}

                    {result.compliance_summary.compliance_percentage !== undefined && (
                      <div className="mt-3">
                        <div className="progress" style={{ height: '24px' }}>
                          <div
                            className={`progress-bar ${result.compliance_summary.compliance_percentage > 80 ? 'bg-success' : result.compliance_summary.compliance_percentage > 50 ? 'bg-warning' : 'bg-danger'}`}
                            style={{ width: `${result.compliance_summary.compliance_percentage}%` }}
                          >
                            {result.compliance_summary.compliance_percentage}% Compliant
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Findings */}
              {result.inspection_findings && (
                <div className="card mb-3">
                  <div className="card-header"><h5 className="mb-0">🔍 Inspection Findings</h5></div>
                  <div className="card-body">
                    {result.inspection_findings.map((finding, i) => (
                      <div key={i} className="border rounded p-3 mb-2">
                        <div className="d-flex justify-content-between align-items-start">
                          <div>
                            <span className={`finding-badge ${finding.severity?.toLowerCase() || 'observation'} me-2`}>
                              {finding.severity}
                            </span>
                            <strong className="ms-1">{finding.category}</strong>
                          </div>
                          <span className={`badge ${finding.status === 'Pass' ? 'bg-success' : 'bg-danger'}`}>
                            {finding.status}
                          </span>
                        </div>
                        <p className="mb-1 mt-2">{finding.description}</p>
                        {finding.applicable_regulation && (
                          <small className="text-muted">
                            📖 {finding.applicable_regulation} {finding.reference_section ? `| ${finding.reference_section}` : ''}
                          </small>
                        )}
                        {finding.recommendation && (
                          <div className="mt-1">
                            <small className="text-primary">→ {finding.recommendation}</small>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Reasoning Chain */}
              {result.compliance_report?.reasoning_chain && (
                <div className="card mb-3">
                  <div className="card-header"><h5 className="mb-0">🔗 Reasoning Chain</h5></div>
                  <div className="card-body">
                    {result.compliance_report.reasoning_chain.map((step, i) => (
                      <div key={i} className="mb-1 small">
                        <span className="text-muted">{step}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Minimum Change Recommendations */}
              {result.compliance_report?.minimum_change_recommendation && (
                <div className="card mb-3">
                  <div className="card-header bg-info bg-opacity-10">
                    <h5 className="mb-0">🔧 Minimum Change Recommendations</h5>
                  </div>
                  <div className="card-body">
                    <p className="small text-muted">{result.compliance_report.minimum_change_recommendation.description}</p>
                    {result.compliance_report.minimum_change_recommendation.priority_items && (
                      <ul className="list-unstyled">
                        {result.compliance_report.minimum_change_recommendation.priority_items.map((item, i) => (
                          <li key={i} className="mb-1">• {item}</li>
                        ))}
                      </ul>
                    )}
                    {result.compliance_report.minimum_change_recommendation.total_estimated_cost && (
                      <p className="fw-semibold mt-2">
                        Estimated Cost: {result.compliance_report.minimum_change_recommendation.total_estimated_cost}
                      </p>
                    )}
                  </div>
                </div>
              )}

              {/* Raw JSON */}
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">📄 Full Report (JSON)</h5>
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
                <span className="fs-1">✅</span>
                <h5 className="mt-3">Generate Compliance Report</h5>
                <p>Enter project details to get an AI-generated, inspector-ready compliance report with traceable reasoning.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Verifier;
