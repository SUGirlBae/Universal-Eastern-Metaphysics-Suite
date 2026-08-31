"""
Root entrypoint for CLI
"""
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent
if str(repo_root / "engine") not in sys.path:
    sys.path.insert(0, str(repo_root / "engine"))
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from engine.cli import main

if __name__ == "__main__":
    main()
