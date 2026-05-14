"""Repository path helpers for scripts run from read_data/."""
from pathlib import Path

READ_DATA_DIR = Path(__file__).resolve().parent
REPO_ROOT = READ_DATA_DIR.parent
HTML_DIR = REPO_ROOT / "html"
