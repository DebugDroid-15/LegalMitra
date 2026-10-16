"""
LegalMitra Production Application Entry Point
Starts the Uvicorn server hosting the LegalMitra AI Chatbot and REST API.
"""

import os
import sys
import uvicorn

if __name__ == "__main__":
    host = os.environ.get("LEGALMITRA_HOST", "127.0.0.1")
    port = int(os.environ.get("LEGALMITRA_PORT", 8000))
    print(f"Starting LegalMitra AI Chatbot on http://{host}:{port}")
    uvicorn.run("legalmitra.web.app:app", host=host, port=port, reload=False)

