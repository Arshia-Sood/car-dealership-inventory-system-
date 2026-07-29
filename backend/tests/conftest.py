import sys
from pathlib import Path

# Ensure the backend root directory is on Python's import path so tests can
# import modules like `from app.main import app`.
BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
