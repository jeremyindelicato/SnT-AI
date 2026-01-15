"""
Start&Trade Backend Application
"""
__version__ = "1.0.0"

# Import main app only when needed (avoid importing FastAPI dependencies for testing)
try:
    from .main import app
    __all__ = ["app"]
except ImportError:
    # Allow importing submodules without FastAPI installed
    pass
