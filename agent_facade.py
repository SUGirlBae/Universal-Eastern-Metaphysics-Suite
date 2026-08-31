"""
Root entrypoint for Agent Facade
"""
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent
if str(repo_root / "engine") not in sys.path:
    sys.path.insert(0, str(repo_root / "engine"))
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from engine.agent_facade import *

if __name__ == "__main__":
    import json
    res = get_agent_payload(question="System Health Check")
    print(json.dumps(res, ensure_ascii=False, indent=2))
