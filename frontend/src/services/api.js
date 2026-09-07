/**
 * API Service - Communication layer between React frontend and FastAPI backend.
 */

import axios from 'axios';

const getDefaultApiUrl = () => {
  if (typeof window === 'undefined') {
    return 'http://localhost:8000/api/v1';
  }

  // CRA runs on port 3000; the API runs on the same host at port 8000.
  // When the frontend is served by FastAPI, use a relative API path instead.
  if (window.location.port === '3000') {
    return `http://${window.location.hostname}:8000/api/v1`;
  }

  return '/api/v1';
};

const API_BASE_URL = process.env.REACT_APP_API_URL || getDefaultApiUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================================
// Knowledge Base
// ============================================================================

export const searchKnowledgeBase = async (query, city = null, category = null, topK = 5) => {
  const response = await api.post('/knowledge-base/search', {
    query,
    city,
    category,
    top_k: topK,
  });
  return response.data;
};

// ============================================================================
// Objective 1: Conflict Resolution
// ============================================================================

export const resolveConflict = async (conflictDescription, city = null, category = null, projectDetails = null) => {
  const response = await api.post('/conflict-resolve', {
    conflict_description: conflictDescription,
    city,
    category,
    project_details: projectDetails,
  });
  return response.data;
};

// ============================================================================
// Objective 2: Time-Aware Prediction
// ============================================================================

export const predictCompliance = async (projectDescription, city = null, timeline = null, permits = null) => {
  const response = await api.post('/predict', {
    project_description: projectDescription,
    city,
    project_timeline: timeline,
    current_permits: permits,
  });
  return response.data;
};

// ============================================================================
// Objective 3: Verification & Reporting
// ============================================================================

export const verifyCompliance = async (projectDescription, city = null, category = null, scope = 'full') => {
  const response = await api.post('/verify', {
    project_description: projectDescription,
    city,
    category,
    scope,
  });
  return response.data;
};

// ============================================================================
// Inspector Chatbot
// ============================================================================

export const getPersonas = async () => {
  const response = await api.get('/chat/personas');
  return response.data;
};

export const chatWithInspector = async (message, persona = 'municipal_engineer', history = []) => {
  const response = await api.post('/chat', {
    message,
    persona,
    history,
  });
  return response.data;
};

// ============================================================================
// System
// ============================================================================

export const getHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const getStats = async () => {
  const response = await api.get('/stats');
  return response.data;
};

export default api;
