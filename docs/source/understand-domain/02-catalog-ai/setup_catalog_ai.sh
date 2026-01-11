#!/bin/bash
# Setup script for AI-Powered Product Catalogs notebook
# Run this before executing the notebook

set -e

echo ""
echo "=== Setting up Ollama ==="

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama already installed: $(ollama --version)"
fi

# Pull the model
echo "Pulling llama3.2 model (this may take a few minutes on first run)..."
ollama pull llama3.2

# Start Ollama server if not running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Starting Ollama server..."
    ollama serve &
    sleep 3
fi

echo ""
echo "=== Verifying setup ==="
curl -s http://localhost:11434/api/tags | head -c 200

echo ""
echo ""
echo "Setup complete! You can now run the notebook."
