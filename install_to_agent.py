#!/usr/bin/env python3
"""
Antigravity Eastern Metaphysics All-In-One Engine & Skill Installer (v3.0.0)
1-Click Automated Multi-Target Installer & Live Synchronizer for AI Agents & Developers.
"""
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent
ENGINE_DIR = REPO_ROOT / "engine"
TOOLS_DIR = REPO_ROOT / "tools"
TESTS_DIR = REPO_ROOT / "tests"
RULES_DIR = REPO_ROOT / "rules"
SKILL_FILE = REPO_ROOT / "SKILL.md"

DEST_BASE = Path.home() / ".gemini" / "config"
DEST_SKILLS_ICHING = DEST_BASE / "skills" / "iching-deep-research"
DEST_SKILLS_TUVI = DEST_BASE / "skills" / "tu-vi-deep-research"
DEST_AIAGENT = Path(r"D:\Book-20251020T041506Z-1-001\AIAgent")
DEST_RULES = DEST_BASE / "rules"

def run_step(msg):
    print(f"\n[{msg}]")

def sync_dir(src: Path, dst: Path):
    if not src.exists():
        return
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".pytest_cache", ".agents"))

def main():
    print("=" * 75)
    print("  ANTIGRAVITY EASTERN METAPHYSICS & UNIVERSAL ZIWEI SUITE (v3.0.0)")
    print("  Multi-Target Live Synchronizer & Verification Engine")
    print("=" * 75)

    # 1. Check Python dependencies
    run_step("1/3] Cài đặt / Kiểm tra thư viện Python...")
    try:
        import lunar_python
        print("  ✓ lunar-python đã sẵn sàng.")
    except ImportError:
        print("  -> Đang cài đặt lunar-python...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "lunar-python"])
        print("  ✓ Cài đặt lunar-python thành công.")

    # 2. Multi-Target Synchronization
    run_step("2/3] Đồng bộ hóa Multi-Target vào các môi trường AI Agent...")
    try:
        from tools.sync_to_aiagent import sync_to_all_targets
        sync_to_all_targets()
    except Exception as e:
        print(f"  -> Chạy dự phòng copy cục bộ (Lỗi helper: {e})...")
        DEST_SKILLS_ICHING.mkdir(parents=True, exist_ok=True)
        DEST_SKILLS_TUVI.mkdir(parents=True, exist_ok=True)
        DEST_RULES.mkdir(parents=True, exist_ok=True)
        
        sync_dir(ENGINE_DIR, DEST_SKILLS_ICHING / "engine")
        sync_dir(TOOLS_DIR, DEST_SKILLS_ICHING / "tools")
        sync_dir(REPO_ROOT / "web", DEST_SKILLS_ICHING / "web")
        shutil.copy2(SKILL_FILE, DEST_SKILLS_ICHING / "SKILL.md")
        
        sync_dir(ENGINE_DIR, DEST_SKILLS_TUVI / "engine")
        sync_dir(TOOLS_DIR, DEST_SKILLS_TUVI / "tools")
        shutil.copy2(SKILL_FILE, DEST_SKILLS_TUVI / "SKILL.md")
        
        if (REPO_ROOT / "tool_definitions.json").exists():
            shutil.copy2(REPO_ROOT / "tool_definitions.json", DEST_SKILLS_ICHING / "tool_definitions.json")
            shutil.copy2(REPO_ROOT / "tool_definitions.json", DEST_SKILLS_TUVI / "tool_definitions.json")
            
        rule_src = RULES_DIR / "iching_divination_rules.md"
        if rule_src.exists():
            shutil.copy2(rule_src, DEST_RULES / "iching_divination_rules.md")

    # 3. Self-Test
    run_step("3/3] Chạy tự kiểm tra toàn diện 100% phân hệ (Self-Test)...")
    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
        
    try:
        from mai_hoa import calculate_mai_hoa_from_time
        from lunar_solar import calculate_time_coordinates
        tc = calculate_time_coordinates(datetime.now())
        calculate_mai_hoa_from_time(tc)
        print("  ✓ Mai Hoa Engine: OK")

        from luc_hao import calculate_full_luc_hao
        mh = calculate_mai_hoa_from_time(tc)
        calculate_full_luc_hao(mh, tc)
        print("  ✓ Lục Hào Dã Hạc Engine: OK")

        from coin_toss import calculate_coin_luc_hao
        calculate_coin_luc_hao([7, 8, 9, 6, 7, 8])
        print("  ✓ 3 Xu Ngũ Đế (0-6 Hào Động): OK")

        from bazi_engine import calculate_bazi
        calculate_bazi(datetime(2025, 6, 20, 10, 0))
        print("  ✓ Tử Bình Bát Tự Engine: OK")

        from tu_vi_advanced import calculate_universal_tu_vi
        tv = calculate_universal_tu_vi(datetime(2025, 6, 20, 10, 0), gender=1, school="standard")
        assert len(tv["palaces"]) == 12
        assert len(tv["flying_stars"]["palace_flying_stars"]) == 12
        print("  ✓ Tử Vi Đẩu Số Đa Phái Toàn Diện (110+ sao, 12 Cung Phi Tinh): OK")

        from ha_lac_engine import calculate_ha_lac
        calculate_ha_lac(datetime(2025, 6, 20, 10, 0))
        print("  ✓ Bát Tự Hà Lạc Engine: OK")

        from ky_mon_engine import calculate_ky_mon
        calculate_ky_mon(datetime(2025, 6, 20, 10, 0))
        print("  ✓ Kỳ Môn Độn Giáp Engine: OK")

        from timing_almanac import scan_target_timing_dates
        scan_target_timing_dates(datetime.now(), ["Tý", "Ngọ"])
        print("  ✓ Trạch Cát Tung Shing & Ứng Kỳ: OK")
        
        from agent_facade import get_agent_payload, compare_ground_truth_canonical_astrolabe, run_ziwei_stress_test
        payload = get_agent_payload(dt=datetime(2025, 6, 20, 10, 0), question="Self test")
        assert "tuvi" in payload["data"]
        print("  ✓ Unified Agent Facade & Structured JSON API: OK")

        stress_res = run_ziwei_stress_test(num_vectors=50)
        assert stress_res["success"] is True
        print("  ✓ Ziwei Stress Test Pipeline (50 vectors benchmark): OK")
        
    except Exception as e:
        print(f"  ✗ Self-Test thất bại: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "=" * 75)
    print("  HOÀN TẤT CÀI ĐẶT & ĐỒNG BỘ HÓA! Bạn có thể sử dụng ngay bằng lệnh:")
    print("  python cli.py --now")
    print("  python cli.py --tu-vi '20/06/2025 10:00' --school kham_thien")
    print("  python cli.py --stress-test 1000")
    print("  python cli.py --compare-gt '<path_to_canonical_astrolabe_file>'")
    print("  python cli.py --vector-gen 100")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    main()
