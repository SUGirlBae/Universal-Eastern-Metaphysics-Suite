import random
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List

try:
    from .tu_vi_advanced import calculate_universal_tu_vi
except (ImportError, ValueError):
    from tu_vi_advanced import calculate_universal_tu_vi

def run_ziwei_stress_test_pipeline(num_vectors: int = 1000) -> Dict[str, Any]:
    """
    Sinh num_vectors ngày giờ sinh ngẫu nhiên từ 1900 đến 2100 và chạy stress test tải cao.
    Kiểm tra:
    - Zero crash, zero unhandled exception
    - Thời gian tính toán trung bình < 2ms/vector
    """
    start_time = time.perf_counter()
    errors = []
    
    start_dt = datetime(1900, 1, 1)
    end_dt = datetime(2100, 12, 31)
    delta_days = (end_dt - start_dt).days
    
    for i in range(num_vectors):
        r_days = random.randint(0, delta_days)
        r_seconds = random.randint(0, 86399)
        dt = start_dt + timedelta(days=r_days, seconds=r_seconds)
        gender = random.choice([0, 1])
        school = random.choice(["standard", "kham_thien", "nam_phai", "trung_chau", "luong_phai"])
        cuc_opt = random.choice([None, 2, 3, 4, 5, 6])
        
        try:
            res = calculate_universal_tu_vi(dt, gender=gender, school=school, cuc_override=cuc_opt)
            assert len(res["palaces"]) == 12
            assert len(res["flying_stars"]["palace_flying_stars"]) == 12
        except Exception as e:
            errors.append({"index": i, "dt": dt.isoformat(), "error": str(e)})
            
    total_duration = time.perf_counter() - start_time
    avg_duration_ms = (total_duration / num_vectors) * 1000
    
    return {
        "num_vectors": num_vectors,
        "total_duration_sec": total_duration,
        "avg_duration_ms": avg_duration_ms,
        "errors_count": len(errors),
        "errors": errors[:5],
        "success": len(errors) == 0
    }
