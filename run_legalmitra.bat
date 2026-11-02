@echo off
TITLE LegalMitra - Indian Legal Intelligence Desktop Edition
color 0B
echo ===============================================================================
echo                LEGALMITRA - INDIAN LEGAL INTELLIGENCE
echo        Offline Sovereign Edition (BNS, BNSS, BSA, High Court & SC)
echo ===============================================================================
echo.

:: 1. Verify Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not found in system PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: 2. Check local model availability
if exist "models\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" (
    echo [OK] Offline Base Model Detected: Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf (4.92 GB)
) else (
    echo [NOTICE] Offline 4-bit model not found in models\ folder.
    echo Operating in deterministic pipeline + mock GGUF mode.
)

if exist "models\legalmitra-lora-adapter.gguf" (
    echo [OK] Fine-Tuned Indian Law LoRA Adapter Detected: legalmitra-lora-adapter.gguf (83.9 MB)
)

echo.
echo [STARTING] Launching LegalMitra FastAPI Engine & Stitch UI...
echo Web UI will be accessible at: http://localhost:8000
echo.

:: 3. Launch browser in background after 2 seconds
start "" powershell -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8000'"

:: 4. Start Uvicorn Server
python -m uvicorn legalmitra.server.api:app --host 127.0.0.1 --port 8000 --log-level info

pause

