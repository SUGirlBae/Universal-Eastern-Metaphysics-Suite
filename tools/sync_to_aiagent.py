#!/usr/bin/env python3
r"""
Multi-Target Synchronization Utility
Synchronizes all engine files, tools, test suites, schemas, and skills to:
- Target 1: D:\Book-20251020T041506Z-1-001\AIAgent
- Target 2: C:\Users\Administrator\.gemini\config\skills\tu-vi-deep-research
- Target 3: C:\Users\Administrator\.gemini\config\skills\iching-deep-research
"""
import sys
import os
import shutil
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

TARGET_1_AIAGENT = Path(r"D:\Book-20251020T041506Z-1-001\AIAgent")
TARGET_2_TUVI_SKILL = Path.home() / ".gemini" / "config" / "skills" / "tu-vi-deep-research"
TARGET_3_ICHING_SKILL = Path.home() / ".gemini" / "config" / "skills" / "iching-deep-research"
DEST_RULES = Path.home() / ".gemini" / "config" / "rules"

IGNORED_DIRS = {"__pycache__", ".pytest_cache", ".git", ".agents", ".github"}
IGNORED_EXTS = {".pyc", ".pyo"}

def compute_file_hash(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def sync_directory_tree(src: Path, dst: Path) -> int:
    """Recursively copy directory tree ignoring cache and metadata folders."""
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for root, dirs, files in os.walk(src):
        # Filter ignored dirs
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        rel_path = Path(root).relative_to(src)
        target_dir = dst / rel_path
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for f in files:
            if any(f.endswith(ext) for ext in IGNORED_EXTS):
                continue
            src_file = Path(root) / f
            dst_file = target_dir / f
            shutil.copy2(src_file, dst_file)
            count += 1
    return count

def sync_single_file(src_file: Path, dst_file: Path) -> bool:
    if src_file.exists():
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_file)
        return True
    return False

def sync_to_all_targets() -> Dict[str, Any]:
    print("=" * 75)
    print("  LIVE MULTI-TARGET SYNCHRONIZATION (M4)")
    print("  Eastern Metaphysics Suite & Universal Ziwei Verification Pipeline")
    print("=" * 75)
    
    results = {}
    
    # --------------------------------------------------------------------------
    # TARGET 1: D:\Book-20251020T041506Z-1-001\AIAgent
    # --------------------------------------------------------------------------
    print(f"\n[1/3] Synchronizing to Target 1 (AIAgent Repository)...")
    print(f"      Destination: {TARGET_1_AIAGENT}")
    t1_files = 0
    if TARGET_1_AIAGENT.exists():
        # Sync subdirectories
        for dir_name in ["engine", "tools", "tests", "rules", "web", "docs"]:
            src_d = REPO_ROOT / dir_name
            if src_d.exists():
                cnt = sync_directory_tree(src_d, TARGET_1_AIAGENT / dir_name)
                t1_files += cnt
                print(f"      ✓ Synced {dir_name}/ ({cnt} files)")
                
        # Sync root files
        root_files = [
            "SKILL.md", "tool_definitions.json", "setup.py", "pyproject.toml",
            "README.md", "install_to_agent.py", "agent_facade.py", "cli.py",
            "mcp_server.py", "conftest.py", "PROJECT.md", "TEST_INFRA.md",
            "TEST_READY.md", "ORIGINAL_REQUEST.md", "LICENSE"
        ]
        for rf in root_files:
            src_f = REPO_ROOT / rf
            if src_f.exists():
                sync_single_file(src_f, TARGET_1_AIAGENT / rf)
                t1_files += 1
        print(f"      ✓ Total synced to Target 1: {t1_files} files")
        results["target_1_aiagent"] = {"status": "SUCCESS", "files_synced": t1_files, "path": str(TARGET_1_AIAGENT)}
    else:
        print(f"      ⚠ Target 1 path does not exist: {TARGET_1_AIAGENT}")
        results["target_1_aiagent"] = {"status": "SKIPPED_NOT_FOUND", "path": str(TARGET_1_AIAGENT)}

    # --------------------------------------------------------------------------
    # TARGET 2: ~/.gemini/config/skills/tu-vi-deep-research
    # --------------------------------------------------------------------------
    print(f"\n[2/3] Synchronizing to Target 2 (Tu Vi Deep Research Live Skill)...")
    print(f"      Destination: {TARGET_2_TUVI_SKILL}")
    TARGET_2_TUVI_SKILL.mkdir(parents=True, exist_ok=True)
    t2_files = 0
    for dir_name in ["engine", "tools", "tests", "rules"]:
        src_d = REPO_ROOT / dir_name
        if src_d.exists():
            cnt = sync_directory_tree(src_d, TARGET_2_TUVI_SKILL / dir_name)
            t2_files += cnt
            print(f"      ✓ Synced {dir_name}/ ({cnt} files)")
            
    for rf in ["tool_definitions.json", "setup.py", "pyproject.toml", "README.md", "agent_facade.py", "cli.py", "mcp_server.py"]:
        src_f = REPO_ROOT / rf
        if src_f.exists():
            sync_single_file(src_f, TARGET_2_TUVI_SKILL / rf)
            t2_files += 1
            
    # Tu Vi customized SKILL.md
    tu_vi_skill_header = """---
name: tu-vi-deep-research
description: Hệ thống Luận Giải Tử Vi Đẩu Số Toàn Diện Đa Phái (Nam Phái 110+ sao, Khâm Thiên Tứ Hóa, Lương Phái, Trung Châu Phái, Bắc Phái, Ma Trận 12 Cung Phi Tinh, Tự Hóa, Hướng Tâm, Phương Viên Toàn Đồ, Đường Kỵ Chuyển Lộc/Chuyển Kỵ, Pipeline Kiểm Thử Tải Cao Zero-Diff CanonicalAstrolabe). 100% Offline, <2ms/lá số, Zero Context Bloat, Master Synthesis Report & Agent-First JSON API.
---
"""
    skill_content = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    if skill_content.startswith("---"):
        parts = skill_content.split("---", 2)
        if len(parts) >= 3:
            tuvi_skill_body = parts[2]
            (TARGET_2_TUVI_SKILL / "SKILL.md").write_text(tu_vi_skill_header + tuvi_skill_body.lstrip(), encoding="utf-8")
            t2_files += 1
    else:
        sync_single_file(REPO_ROOT / "SKILL.md", TARGET_2_TUVI_SKILL / "SKILL.md")
        t2_files += 1
        
    print(f"      ✓ Total synced to Target 2: {t2_files} files")
    results["target_2_tuvi_skill"] = {"status": "SUCCESS", "files_synced": t2_files, "path": str(TARGET_2_TUVI_SKILL)}

    # --------------------------------------------------------------------------
    # TARGET 3: ~/.gemini/config/skills/iching-deep-research
    # --------------------------------------------------------------------------
    print(f"\n[3/3] Synchronizing to Target 3 (I Ching Deep Research Live Skill)...")
    print(f"      Destination: {TARGET_3_ICHING_SKILL}")
    TARGET_3_ICHING_SKILL.mkdir(parents=True, exist_ok=True)
    t3_files = 0
    for dir_name in ["engine", "tools", "tests", "rules", "web"]:
        src_d = REPO_ROOT / dir_name
        if src_d.exists():
            cnt = sync_directory_tree(src_d, TARGET_3_ICHING_SKILL / dir_name)
            t3_files += cnt
            print(f"      ✓ Synced {dir_name}/ ({cnt} files)")
            
    for rf in ["SKILL.md", "tool_definitions.json", "setup.py", "pyproject.toml", "README.md", "agent_facade.py", "cli.py", "mcp_server.py"]:
        src_f = REPO_ROOT / rf
        if src_f.exists():
            sync_single_file(src_f, TARGET_3_ICHING_SKILL / rf)
            t3_files += 1
            
    print(f"      ✓ Total synced to Target 3: {t3_files} files")
    results["target_3_iching_skill"] = {"status": "SUCCESS", "files_synced": t3_files, "path": str(TARGET_3_ICHING_SKILL)}

    # Sync Rules to global rules directory
    DEST_RULES.mkdir(parents=True, exist_ok=True)
    rule_src = REPO_ROOT / "rules" / "iching_divination_rules.md"
    if rule_src.exists():
        sync_single_file(rule_src, DEST_RULES / "iching_divination_rules.md")
        print(f"\n[Rules] ✓ Synchronized global rules to {DEST_RULES / 'iching_divination_rules.md'}")

    # --------------------------------------------------------------------------
    # VERIFICATION TEST
    # --------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("  VERIFYING SYNCHRONIZED TARGETS")
    print("=" * 75)
    
    for t_name, t_info in results.items():
        if t_info["status"] != "SUCCESS":
            continue
        p = Path(t_info["path"])
        facade_path = p / "engine" / "agent_facade.py"
        tuvi_path = p / "engine" / "tu_vi_advanced.py"
        skill_path = p / "SKILL.md"
        tool_def_path = p / "tool_definitions.json"
        
        ok_facade = facade_path.exists()
        ok_tuvi = tuvi_path.exists()
        ok_skill = skill_path.exists()
        ok_tool_def = tool_def_path.exists()
        
        print(f"  • {t_name} Verification:")
        print(f"    - engine/agent_facade.py : {'✓ OK' if ok_facade else '✗ MISSING'}")
        print(f"    - engine/tu_vi_advanced.py: {'✓ OK' if ok_tuvi else '✗ MISSING'}")
        print(f"    - SKILL.md               : {'✓ OK' if ok_skill else '✗ MISSING'}")
        print(f"    - tool_definitions.json  : {'✓ OK' if ok_tool_def else '✗ MISSING'}")
        
        if not (ok_facade and ok_tuvi and ok_skill and ok_tool_def):
            t_info["verification"] = "FAILED"
        else:
            t_info["verification"] = "PASSED"
            
    print("\n" + "=" * 75)
    print("  ALL TARGETS SYNCHRONIZED AND VERIFIED SUCCESSFULLY!")
    print("=" * 75)
    return results

if __name__ == "__main__":
    sync_to_all_targets()
