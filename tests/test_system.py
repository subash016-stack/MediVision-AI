import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, backend_path)
os.chdir(backend_path)

print("--- Testing Backend Modules & System Integrity ---", flush=True)

try:
    print("1. Testing FastAPI and Route Registrations...", flush=True)
    from main import app
    routes = [getattr(r, 'path', getattr(r, 'path_format', str(r))) for r in app.routes]
    print(f"   [PASS] FastAPI initialized with {len(routes)} route entries.", flush=True)

    print("2. Testing Schemas Validation...", flush=True)
    from schemas.profile import UpdateProfile
    from schemas.change_password import ChangePassword
    from schemas.review import ReviewRequest
    
    p = UpdateProfile(full_name="Test User", phone="1234567890")
    cp = ChangePassword(current_password="oldpass", new_password="newsecurepass")
    rr = ReviewRequest(doctor_comments="Clinical assessment verified.")
    print("   [PASS] Pydantic schemas validated successfully.", flush=True)

    print("3. Testing AI & Grad-CAM Imports...", flush=True)
    from ai.labels import CLASS_NAMES
    from ai.model_loader import get_model
    from ai.gradcam import find_last_conv_layer
    print(f"   [PASS] AI Labels loaded: {CLASS_NAMES}", flush=True)

    print("4. Testing Database Connection Module...", flush=True)
    from database.connection import get_collection
    users_col = get_collection("users")
    print(f"   [PASS] Database collection handle acquired: {users_col.name}", flush=True)

    print("\n>>> ALL BACKEND SYSTEM CHECKS PASSED SUCCESSFULLY! <<<", flush=True)

except Exception as e:
    print(f"\n[FAIL] Backend error detected: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
