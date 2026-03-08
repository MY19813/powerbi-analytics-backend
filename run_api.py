import uvicorn
from pathlib import Path
import sys

# Add api directory to path
api_dir = Path(__file__).parent / "api"
sys.path.insert(0, str(api_dir.parent))

if __name__ == "__main__":
    print("=" * 60)
    print("STARTING POWERBI ANALYTICS API")
    print("=" * 60)
    print("\n📊 API Documentation:")
    print("  - Swagger UI: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("\n🚀 Starting server...\n")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )