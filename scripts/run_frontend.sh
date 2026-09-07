#!/bin/bash
# ============================================================================
# Start the Multi-Agent Legal RAG Frontend Server
# ============================================================================

echo "=========================================="
echo "Multi-Agent Legal RAG - Frontend Server"
echo "=========================================="

cd frontend

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start development server
echo "Starting React development server on http://localhost:3000"
echo ""
npm start
