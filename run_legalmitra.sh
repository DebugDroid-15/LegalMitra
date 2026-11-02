#!/bin/bash
echo "==============================================================================="
echo "               LEGALMITRA - INDIAN LEGAL INTELLIGENCE"
echo "       Offline Sovereign Edition (BNS, BNSS, BSA, High Court & SC)"
echo "==============================================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found. Please install Python 3.10+."
    exit 1
fi

if [ -f "models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" ]; then
    echo "[OK] Offline Base Model: Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf (4.92 GB)"
fi

if [ -f "models/legalmitra-lora-adapter.gguf" ]; then
    echo "[OK] LoRA Adapter: legalmitra-lora-adapter.gguf (83.9 MB)"
fi

echo ""
echo "[STARTING] Launching LegalMitra Server on http://127.0.0.1:8000..."

# Auto-open browser
if command -v xdg-open &> /dev/null; then
    (sleep 2 && xdg-open "http://localhost:8000") &
elif command -v open &> /dev/null; then
    (sleep 2 && open "http://localhost:8000") &
fi

python3 -m uvicorn legalmitra.server.api:app --host 127.0.0.1 --port 8000 --log-level info

