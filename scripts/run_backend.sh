#!/bin/bash
# ============================================================================
# Start the Multi-Agent Legal RAG Backend Server
# ============================================================================

echo "=========================================="
echo "Multi-Agent Legal RAG - Backend Server"
echo "=========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 not found. Please install Python 3.9+"
    exit 1
fi

# Check if virtual environment exists
if [ -d ".venv" ]; then
    VENV_DIR=".venv"
elif [ -d "venv" ]; then
    VENV_DIR="venv"
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    VENV_DIR=".venv"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Check GROQ API KEY
if [ -z "$GROQ_API_KEY" ] && [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  WARNING: GROQ_API_KEY not set!"
    echo "Set it with: export GROQ_API_KEY='your_key_here'"
    echo "Or create a .env file with GROQ_API_KEY=your_key_here"
    echo ""
fi

# Index knowledge base if needed
echo "Checking knowledge base..."
python3 -c "
import sys
sys.path.insert(0, '.')
from backend.services.knowledge_base_service import kb_service
stats = kb_service.get_collection_stats()
if stats['status'] == 'empty':
    print('Indexing knowledge base...')
    count = kb_service.index_knowledge_base()
    print(f'Indexed {count} documents')
else:
    print(f'Knowledge base ready: {stats[\"total_documents\"]} documents')
"

# Start server
echo ""
echo "Starting FastAPI server on http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo ""
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
