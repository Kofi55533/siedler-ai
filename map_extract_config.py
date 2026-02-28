from pathlib import Path
import os

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_EXTRACT_DIR = REPO_ROOT / "map_extract" / "wintersturm_extracted"

# Optional override for advanced workflows
EXTRACTED_DIR = Path(os.environ.get("SIEDLER_MAP_EXTRACT_DIR", DEFAULT_EXTRACT_DIR))
