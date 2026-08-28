import sys
from pathlib import Path

# Ensure backend is in path
backend_path = Path(__file__).parent.resolve()
sys.path.insert(0, str(backend_path))

try:
    from app.main import app
    print("SUCCESS: FastAPI Application initialized successfully!")
    print("SUCCESS: All modules imported without syntax errors.")
    
    # Inspect registered routes
    routes = [route.path for route in app.routes]
    print(f"Registered {len(routes)} routes.")
except Exception as e:
    print(f"FAILED: Application failed to initialize.")
    print(e)
    import traceback
    traceback.print_exc()
    sys.exit(1)
