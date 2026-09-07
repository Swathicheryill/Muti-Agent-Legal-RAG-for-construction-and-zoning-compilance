# 🏗️ Multi-Agent Legal RAG: Construction & Zoning Compliance

An AI-powered multi-agent system for autonomous compliance analysis of construction and zoning regulations across Indian metropolitan cities.

## 🎯 Objectives

### Objective 1: Conflict Resolution Agent
Resolves contradictory legal requirements across overlapping jurisdictions (local → state → federal) using specialized legal-parsing agents trained on 5,500+ conflict scenarios.

### Objective 2: Time-Aware Prediction Agent
Predicts future compliance violations (6-12 months ahead) using 5,000+ historical code changes and construction timelines, outputting probabilistic compliance roadmaps with confidence intervals.

### Objective 3: Verification & Reporting Agent
Produces inspector-ready, legally defensible compliance reports with traceable reasoning chains, trained on 3,500+ annotated construction scenarios.

## 🏙️ Coverage

### Cities
| City | State | Building Authority | Key Laws |
|------|-------|--------------------|----------|
| Bangalore | Karnataka | BBMP | Karnataka TCP Act, 1961 |
| Chennai | Tamil Nadu | GCC/CMDA | TN Building Rules, 2019 |
| Delhi | Delhi | MCD/DDA | Delhi Building Bye-Laws 2021 |
| Mumbai | Maharashtra | BMC | MRTP Act, 1966 |
| Hyderabad | Telangana | GHMC/HMDA | TS Building Rules, 2012 |

### Law Categories
- 🏗️ **Building Construction** - Plans, approvals, FAR, setbacks, parking
- 🌿 **Environment** - EIA, CRZ, pollution control, waste management
- 💧 **Water** - Supply, rainwater harvesting, STP, groundwater
- 🌬️ **Air** - Quality standards, emission control, dust management
- 🛣️ **Road & Infrastructure** - Width, access, metro buffers, highways
- 🏠 **Housing** - RERA, affordable housing, PMAY, MHADA
- 🏭 **Industry** - Zoning, fire safety, CETP, buffer zones
- 📐 **Area/Zoning** - Land use, heritage zones, airport restrictions

## 📊 Datasets

| Dataset | Count | File |
|---------|-------|------|
| Knowledge Base Laws | 67+ | `datasets/knowledge_base/` |
| Conflict Scenarios | 5,500 | `datasets/objective1_conflict/` |
| Historical Changes | 2,500 | `datasets/objective2_prediction/` |
| Prediction Scenarios | 2,500 | `datasets/objective2_prediction/` |
| Verification Reports | 3,500 | `datasets/objective3_verification/` |

## 🛠️ Tech Stack

### Backend
- **FastAPI** - REST API framework
- **Groq** - LLM inference (LLaMA 3.3 70B, Mixtral 8x7B)
- **ChromaDB** - Vector database for RAG
- **sentence-transformers** - Text embeddings (all-MiniLM-L6-v2)
- **LangChain** - LLM orchestration

### Frontend
- **React 18** - UI framework
- **React Router** - Navigation
- **Bootstrap 5** - CSS framework
- **Axios** - HTTP client

### Training
- **PyTorch** - Deep learning framework
- **PEFT/LoRA** - Parameter-efficient fine-tuning
- **BitsAndBytes** - Quantization for memory efficiency
- **TRL** - Training with reinforcement learning

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API key (get from [console.groq.com](https://console.groq.com))

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd multi_legal_rag

# Setup environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..
```

### 2. Generate Datasets

```bash
python3 scripts/generate_datasets.py
```

### 3. Start Backend

```bash
# Terminal 1: Backend
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will:
1. Automatically index the knowledge base on first startup
2. Start the API server on `http://localhost:8000`
3. API documentation available at `http://localhost:8000/docs`

### 4. Start Frontend

```bash
# Terminal 2: Frontend
cd frontend && npm start
```

The frontend will open at `http://localhost:3000`.

## 📡 API Endpoints

### Health & System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | System health check |
| GET | `/api/v1/stats` | System statistics |

### Knowledge Base
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/knowledge-base/search` | Search the knowledge base |
| POST | `/api/v1/knowledge-base/index` | Re-index knowledge base |

### Objective 1: Conflict Resolution
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/conflict-resolve` | Resolve a jurisdictional conflict |
| POST | `/api/v1/conflict-resolve/async` | Async conflict resolution |

### Objective 2: Time Prediction
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/predict` | Predict future violations |
| POST | `/api/v1/predict/async` | Async prediction |

### Objective 3: Verification
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/verify` | Generate compliance report |
| POST | `/api/v1/verify/async` | Async report generation |

### Inspector Chatbot
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/chat/personas` | Get available personas |
| POST | `/api/v1/chat` | Chat with inspector |

### Unified
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/compliance-check` | Full 3-agent compliance check |

## 🎨 Frontend Pages

1. **Dashboard** - Overview of system capabilities
2. **Conflict Resolver** - Analyze jurisdictional conflicts
3. **Time Predictor** - Predict future compliance risks
4. **Verifier** - Generate compliance reports
5. **Inspector Chat** - Chat with AI inspectors (4 personas)
6. **Knowledge Base** - Search construction laws

## 🤖 AI Agents

| Agent | Role | Model | Temperature |
|-------|------|-------|-------------|
| Conflict Resolver | Resolves jurisdictional conflicts | LLaMA 3.3 70B | 0.2 |
| Time Predictor | Predicts future violations | LLaMA 3.3 70B | 0.4 |
| Verifier | Generates compliance reports | LLaMA 3.3 70B | 0.1 |
| Inspector Chat | Interactive compliance Q&A | LLaMA 3.3 70B | 0.5 |
| Legal Parser | Parses legal documents | LLaMA 3.1 8B | 0.1 |

## 🧑‍💼 Chat Personas

1. **Er. Rajesh Kumar** - Chief Municipal Engineer (Building Plans, FAR, Setbacks)
2. **Dr. Priya Sharma** - Environmental Compliance Officer (EIA, CRZ, Pollution)
3. **Capt. Vikram Singh** - Fire Safety Officer (Fire NOC, Safety Systems)
4. **Adv. Lakshmi Iyer** - Construction Law Advisor (RERA, Legal Risk)

## 🔧 Training

```bash
# Prepare training data only
python3 training/train_model.py

# Full training (requires GPU)
python3 training/train_model.py --train
```

## 📁 Project Structure

```
multi_legal_rag/
├── datasets/
│   ├── knowledge_base/          # 67+ Indian construction laws
│   ├── objective1_conflict/     # 5,500 conflict scenarios
│   ├── objective2_prediction/   # 5,000 prediction scenarios
│   └── objective3_verification/ # 3,500 verification scenarios
├── backend/
│   ├── agents/                  # AI agent implementations
│   │   ├── conflict_resolver.py
│   │   ├── time_predictor.py
│   │   ├── verifier.py
│   │   └── inspector_chatbot.py
│   ├── services/                # Core services
│   │   ├── groq_service.py      # Groq API integration
│   │   ├── knowledge_base_service.py
│   │   └── rag_engine.py
│   ├── api/
│   │   └── routes.py            # FastAPI routes
│   └── main.py                  # Application entry
├── frontend/
│   ├── src/
│   │   ├── pages/               # React pages
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   └── styles/
│   │       └── main.css         # Custom styles
│   └── public/
├── training/
│   └── train_model.py           # Training pipeline
├── config/
│   └── settings.py              # Configuration
├── scripts/
│   ├── run_backend.sh
│   ├── run_frontend.sh
│   └── generate_datasets.py
└── requirements.txt
```

## 🌍 Future Enhancements

- [ ] Add more Indian cities (Pune, Kolkata, Ahmedabad, Jaipur)
- [ ] International expansion (Singapore, UAE, UK, USA)
- [ ] PDF report generation
- [ ] Multi-language support (Hindi, Tamil, Telugu, Kannada)
- [ ] Real-time code change monitoring
- [ ] Court order tracking integration
- [ ] Mobile app (React Native)
- [ ] Advanced visualization dashboards
- [ ] Integration with satellite imagery for site inspection
- [ ] Blockchain-based compliance certificate

## 📄 License

This project is for educational and research purposes.

---

**Powered by Groq LLM • ChromaDB • FastAPI • React**
