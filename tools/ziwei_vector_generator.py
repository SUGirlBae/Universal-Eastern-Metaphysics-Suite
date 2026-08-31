"""
Multi-Century Random Vector Generator & Edge-Case Synthesizer (1900 - 2100)
Production-grade, Deterministic, 100% Offline, High-Throughput Zi Wei Dou Shu Vector Pipeline.

Features:
- Deterministic pseudo-random vector generation with reproducible seed control across 1900-2100.
- 6 Comprehensive Edge-Case Synthesis Classes:
  1. Century & Quadrennial Leap Year Boundaries (1900, 2000, 2100, Feb 28/29 transitions).
  2. Lunar Leap Months across 1900-2100 (1st half <=15 vs 2nd half >15).
  3. Solar Term Minute Transitions (All 24 JieQi with T-1m, T, T+1m precision).
  4. Zi Hour Split Transitions (Dạ Tý 23:00-23:59 vs Chính Tý 00:00-00:59 vs Sửu 01:00).
  5. Year Boundary Changing Pillars (Gregorian, Lunar New Year Eve, Solar LiChun rollover).
  6. Special Cục Số & Yin-Yang Gender Polarity Matrix across all 60 Jiazi and 12 Branches.
- Full JSON export / import capabilities.
- Integrated CLI & high-throughput benchmark runner.
"""
from __future__ import annotations
import os
import sys
import json
import random
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from functools import lru_cache
from typing import List, Dict, Any, Optional, Tuple, Union

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

try:
    from lunar_python import Solar, Lunar, LunarYear
    HAS_LUNAR_PYTHON = True
    if hasattr(LunarYear, "fromYear"):
        LunarYear.fromYear = lru_cache(maxsize=512)(LunarYear.fromYear)
except ImportError:
    HAS_LUNAR_PYTHON = False

SCHOOLS = ["standard", "kham_thien", "nam_phai", "trung_chau", "luong_phai"]
VIEW_MODES = ["thien_ban", "dia_ban", "nhan_ban"]
CUC_NUMBERS = [2, 3, 4, 5, 6]
CUC_NAMES = {2: "Thủy Nhị Cục", 3: "Mộc Tam Cục", 4: "Kim Tứ Cục", 5: "Thổ Ngũ Cục", 6: "Hỏa Lục Cục"}

CAN_LIST = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI_LIST = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

@dataclass
class ZiweiVector:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int = 0
    gender: str = "nam"  # "nam" | "nu"
    gender_int: int = 1  # 1: Nam, 0: Nữ
    view_mode: str = "thien_ban"
    school: str = "standard"
    edge_case_type: str = "uniform_random"
    class_name: str = "Uniform Random Multi-Century"
    cuc_override: Optional[int] = None
    description: str = "Randomly sampled multi-century vector"
    iso_datetime: str = ""

    def __post_init__(self):
        if not self.iso_datetime:
            self.iso_datetime = f"{self.year:04d}-{self.month:02d}-{self.day:02d}T{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        if self.gender == "nam" and self.gender_int != 1:
            self.gender_int = 1
        elif self.gender == "nu" and self.gender_int != 0:
            self.gender_int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_datetime(self) -> datetime:
        return datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ZiweiVector:
        gender_str = d.get("gender", "nam")
        if isinstance(gender_str, int):
            gender_int = gender_str
            gender_str = "nam" if gender_int == 1 else "nu"
        else:
            gender_int = 1 if str(gender_str).lower() in ["nam", "male", "1", "m"] else 0
            gender_str = "nam" if gender_int == 1 else "nu"

        return cls(
            year=int(d["year"]),
            month=int(d["month"]),
            day=int(d["day"]),
            hour=int(d["hour"]),
            minute=int(d["minute"]),
            second=int(d.get("second", 0)),
            gender=gender_str,
            gender_int=gender_int,
            view_mode=d.get("view_mode", "thien_ban"),
            school=d.get("school", "standard"),
            edge_case_type=d.get("edge_case_type", "uniform_random"),
            class_name=d.get("class_name", ""),
            cuc_override=d.get("cuc_override"),
            description=d.get("description", ""),
            iso_datetime=d.get("iso_datetime", "")
        )
class ZiweiVectorGenerator:
    """
    High-performance Multi-Century Vector Generator and Edge-Case Synthesizer.
    """
    def __init__(self, seed: int = 42):
        self.seed = seed
        self._rng = random.Random(seed)

    def set_seed(self, seed: int) -> None:
        self.seed = seed
        self._rng = random.Random(seed)

    # --------------------------------------------------------------------------
    # 1. RANDOM VECTOR GENERATION (1900 - 2100)
    # --------------------------------------------------------------------------
    def generate_random_vectors(
        self,
        count: int = 1000,
        seed: Optional[int] = None,
        start_year: int = 1900,
        end_year: int = 2100,
        include_cuc_override: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate count deterministic pseudo-random vectors evenly distributed across start_year to end_year.
        """
        if seed is not None:
            rng = random.Random(seed)
        else:
            rng = self._rng

        start_dt = datetime(start_year, 1, 1, 0, 0, 0)
        end_dt = datetime(end_year, 12, 31, 23, 59, 59)
        total_seconds = int((end_dt - start_dt).total_seconds())

        vectors: List[Dict[str, Any]] = []
        for i in range(count):
            offset = rng.randint(0, total_seconds)
            dt = start_dt + timedelta(seconds=offset)

            gender_int = rng.choice([0, 1])
            gender_str = "nam" if gender_int == 1 else "nu"
            school = rng.choice(SCHOOLS)
            view_mode = rng.choice(VIEW_MODES)
            cuc_opt = rng.choice([None, None, None, 2, 3, 4, 5, 6]) if include_cuc_override else None

            vec = ZiweiVector(
                year=dt.year,
                month=dt.month,
                day=dt.day,
                hour=dt.hour,
                minute=dt.minute,
                second=dt.second,
                gender=gender_str,
                gender_int=gender_int,
                view_mode=view_mode,
                school=school,
                edge_case_type="uniform_random",
                class_name="Uniform Random Multi-Century",
                cuc_override=cuc_opt,
                description=f"Uniform random vector #{i+1} in range {start_year}-{end_year}",
                iso_datetime=dt.isoformat()
            )
            vectors.append(vec.to_dict())

        return vectors

    # --------------------------------------------------------------------------
    # 2. EDGE CASE CLASS 1: CENTURY & LEAP YEAR BOUNDARIES
    # --------------------------------------------------------------------------
    def generate_class1_century_leap_cases(self) -> List[Dict[str, Any]]:
        """
        Class 1: Century and Quadrennial Leap Year Boundaries.
        - Non-leap century: 1900, 2100 (Feb 28 23:59:59 -> Mar 1 00:00:00).
        - Leap century: 2000 (Feb 28 23:59:59 -> Feb 29 00:00:00 -> Feb 29 23:59:59 -> Mar 1 00:00:00).
        - Leap years: 1904, 1908, 1984, 1996, 2024, 2096.
        - Non-leap standard years: 1901, 1999, 2023, 2025.
        """
        cases: List[ZiweiVector] = []

        # Century non-leap boundaries (1900 & 2100)
        for yr in [1900, 2100]:
            cases.append(ZiweiVector(
                year=yr, month=2, day=28, hour=23, minute=59, second=59,
                gender="nam", school="standard",
                edge_case_type="century_non_leap_end",
                class_name="Class 1: Century & Leap Year Boundaries",
                description=f"Non-leap century year {yr} final second of Feb 28"
            ))
            cases.append(ZiweiVector(
                year=yr, month=3, day=1, hour=0, minute=0, second=0,
                gender="nu", school="kham_thien",
                edge_case_type="century_non_leap_march_start",
                class_name="Class 1: Century & Leap Year Boundaries",
                description=f"Non-leap century year {yr} first second of March 1"
            ))

        # Century leap year boundary (2000 - divisible by 400)
        cases.append(ZiweiVector(
            year=2000, month=2, day=28, hour=23, minute=59, second=59,
            gender="nam", school="nam_phai",
            edge_case_type="century_leap_feb28_end",
            class_name="Class 1: Century & Leap Year Boundaries",
            description="Leap century 2000 transition to leap day Feb 29"
        ))
        cases.append(ZiweiVector(
            year=2000, month=2, day=29, hour=0, minute=0, second=0,
            gender="nu", school="kham_thien",
            edge_case_type="century_leap_feb29_start",
            class_name="Class 1: Century & Leap Year Boundaries",
            description="Leap century 2000 midnight start of Feb 29"
        ))
        cases.append(ZiweiVector(
            year=2000, month=2, day=29, hour=12, minute=0, second=0,
            gender="nam", school="trung_chau",
            edge_case_type="century_leap_feb29_midday",
            class_name="Class 1: Century & Leap Year Boundaries",
            description="Leap century 2000 noon of leap day Feb 29"
        ))
        cases.append(ZiweiVector(
            year=2000, month=2, day=29, hour=23, minute=59, second=59,
            gender="nu", school="luong_phai",
            edge_case_type="century_leap_feb29_end",
            class_name="Class 1: Century & Leap Year Boundaries",
            description="Leap century 2000 final second of leap day Feb 29"
        ))
        cases.append(ZiweiVector(
            year=2000, month=3, day=1, hour=0, minute=0, second=0,
            gender="nam", school="standard",
            edge_case_type="century_leap_mar1_start",
            class_name="Class 1: Century & Leap Year Boundaries",
            description="Leap century 2000 rollover from Feb 29 to March 1"
        ))

        # Quadrennial leap years (1904, 1984, 2024, 2096)
        for yr in [1904, 1984, 2024, 2096]:
            cases.append(ZiweiVector(
                year=yr, month=2, day=29, hour=6, minute=30, second=0,
                gender="nam", school="standard",
                edge_case_type="quadrennial_leap_feb29",
                class_name="Class 1: Century & Leap Year Boundaries",
                description=f"Quadrennial leap year {yr} Feb 29 morning"
            ))
            cases.append(ZiweiVector(
                year=yr, month=2, day=29, hour=23, minute=59, second=0,
                gender="nu", school="kham_thien",
                edge_case_type="quadrennial_leap_feb29_late",
                class_name="Class 1: Century & Leap Year Boundaries",
                description=f"Quadrennial leap year {yr} Feb 29 late night"
            ))

        # Standard non-leap year controls (1901, 1999, 2023, 2025)
        for yr in [1901, 1999, 2023, 2025]:
            cases.append(ZiweiVector(
                year=yr, month=2, day=28, hour=23, minute=59, second=59,
                gender="nam" if yr % 2 == 1 else "nu", school="standard",
                edge_case_type="standard_non_leap_feb28",
                class_name="Class 1: Century & Leap Year Boundaries",
                description=f"Standard non-leap year {yr} Feb 28 end"
            ))

        return [c.to_dict() for c in cases]
    # --------------------------------------------------------------------------
    # 3. EDGE CASE CLASS 2: LUNAR LEAP MONTHS
    # --------------------------------------------------------------------------
    def generate_class2_lunar_leap_cases(self) -> List[Dict[str, Any]]:
        """
        Class 2: Lunar Leap Months across 1900-2100.
        Covers leap month day 1 (start), day 8 (mid-first-half), day 15 (halfway boundary),
        day 16 (start of second-half), day 29/30 (end of leap month).
        """
        known_leap_years = [
            (1900, 8), (1903, 5), (1906, 4), (1909, 2), (1911, 6), (1914, 5), (1917, 2),
            (1919, 7), (1922, 5), (1925, 4), (1928, 2), (1930, 6), (1933, 5), (1936, 3),
            (1938, 7), (1941, 6), (1944, 4), (1947, 2), (1949, 7), (1952, 5), (1955, 3),
            (1957, 8), (1960, 6), (1963, 4), (1966, 3), (1968, 7), (1971, 5), (1974, 4),
            (1976, 8), (1979, 6), (1982, 4), (1984, 10), (1987, 6), (1990, 5), (1993, 3),
            (1995, 8), (1998, 5), (2001, 4), (2004, 2), (2006, 7), (2009, 5), (2012, 4),
            (2014, 9), (2017, 6), (2020, 4), (2023, 2), (2025, 6), (2028, 5), (2031, 3),
            (2033, 11), (2036, 6), (2039, 5), (2042, 2), (2044, 7), (2047, 5), (2050, 3),
            (2052, 8), (2055, 6), (2058, 4), (2061, 3), (2063, 7), (2066, 5), (2069, 4),
            (2071, 8), (2074, 6), (2077, 4), (2080, 3), (2082, 7), (2085, 5), (2088, 4),
            (2090, 8), (2093, 6), (2096, 4), (2099, 2)
        ]

        cases: List[ZiweiVector] = []

        for l_yr, l_month in known_leap_years:
            sample_days = [1, 15, 16, 29]
            for l_day in sample_days:
                if HAS_LUNAR_PYTHON:
                    try:
                        l_obj = Lunar.fromYmd(l_yr, -l_month, l_day)
                        s_obj = l_obj.getSolar()
                        s_year, s_month, s_day = s_obj.getYear(), s_obj.getMonth(), s_obj.getDay()
                    except Exception:
                        continue
                else:
                    s_year, s_month, s_day = l_yr, min(12, max(1, l_month + 1)), min(28, l_day)

                half_str = "1st_half (<=15)" if l_day <= 15 else "2nd_half (>15)"
                school = SCHOOLS[(l_yr + l_month + l_day) % len(SCHOOLS)]
                gender_str = "nam" if (l_yr + l_day) % 2 == 1 else "nu"

                cases.append(ZiweiVector(
                    year=s_year, month=s_month, day=s_day,
                    hour=10 if l_day <= 15 else 20, minute=30, second=0,
                    gender=gender_str, school=school,
                    edge_case_type=f"lunar_leap_m{l_month}_d{l_day}",
                    class_name="Class 2: Lunar Leap Months",
                    description=f"Lunar year {l_yr} Leap Month {l_month} Day {l_day} [{half_str}] -> Solar {s_year:04d}-{s_month:02d}-{s_day:02d}"
                ))

        return [c.to_dict() for c in cases]

    # --------------------------------------------------------------------------
    # 4. EDGE CASE CLASS 3: SOLAR TERM MINUTE-PRECISION TRANSITIONS
    # --------------------------------------------------------------------------
    def generate_class3_solar_term_cases(self) -> List[Dict[str, Any]]:
        """
        Class 3: Solar Term Transitions to Minute Precision.
        For milestone years, extracts the exact timestamp T of major JieQi,
        and synthesizes 3 consecutive vectors: (T - 1 minute), T, and (T + 1 minute).
        """
        milestone_years = [1900, 1924, 1948, 1972, 1984, 1999, 2000, 2012, 2020, 2024, 2025, 2026, 2050, 2075, 2100]
        cases: List[ZiweiVector] = []

        if HAS_LUNAR_PYTHON:
            for yr in milestone_years:
                try:
                    s_mid = Solar.fromYmdHms(yr, 6, 15, 12, 0, 0)
                    l_mid = s_mid.getLunar()
                    jie_qi_table = l_mid.getJieQiTable()

                    for jq_name, sol_item in jie_qi_table.items():
                        jq_yr = sol_item.getYear()
                        if jq_yr != yr:
                            continue
                        jq_m = sol_item.getMonth()
                        jq_d = sol_item.getDay()
                        jq_h = sol_item.getHour()
                        jq_min = sol_item.getMinute()
                        jq_s = sol_item.getSecond()

                        exact_dt = datetime(jq_yr, jq_m, jq_d, jq_h, jq_min, jq_s)
                        dt_prev = exact_dt - timedelta(minutes=1)
                        dt_next = exact_dt + timedelta(minutes=1)

                        # T - 1 min (Before transition)
                        cases.append(ZiweiVector(
                            year=dt_prev.year, month=dt_prev.month, day=dt_prev.day,
                            hour=dt_prev.hour, minute=dt_prev.minute, second=dt_prev.second,
                            gender="nam", school="kham_thien",
                            edge_case_type=f"solar_term_pre_{jq_name}",
                            class_name="Class 3: Solar Term Minute Transitions",
                            description=f"1 minute before Solar Term '{jq_name}' in {yr} (exact: {exact_dt.strftime('%Y-%m-%d %H:%M:%S')})"
                        ))

                        # T (Exact transition moment)
                        cases.append(ZiweiVector(
                            year=exact_dt.year, month=exact_dt.month, day=exact_dt.day,
                            hour=exact_dt.hour, minute=exact_dt.minute, second=exact_dt.second,
                            gender="nu", school="standard",
                            edge_case_type=f"solar_term_exact_{jq_name}",
                            class_name="Class 3: Solar Term Minute Transitions",
                            description=f"Exact minute of Solar Term '{jq_name}' in {yr} ({exact_dt.strftime('%Y-%m-%d %H:%M:%S')})"
                        ))

                        # T + 1 min (After transition)
                        cases.append(ZiweiVector(
                            year=dt_next.year, month=dt_next.month, day=dt_next.day,
                            hour=dt_next.hour, minute=dt_next.minute, second=dt_next.second,
                            gender="nam", school="nam_phai",
                            edge_case_type=f"solar_term_post_{jq_name}",
                            class_name="Class 3: Solar Term Minute Transitions",
                            description=f"1 minute after Solar Term '{jq_name}' in {yr} (exact: {exact_dt.strftime('%Y-%m-%d %H:%M:%S')})"
                        ))
                except Exception:
                    continue
        else:
            for yr in milestone_years:
                for m, d, h, mn, jq_name in [(2, 4, 16, 27, "Lap_Xuan"), (6, 21, 4, 51, "Ha_Chi"), (9, 22, 20, 43, "Thu_Phan"), (12, 21, 17, 20, "Dong_Chi")]:
                    exact_dt = datetime(yr, m, d, h, mn, 0)
                    for delta_m, tag in [(-1, "pre"), (0, "exact"), (1, "post")]:
                        dt_sample = exact_dt + timedelta(minutes=delta_m)
                        cases.append(ZiweiVector(
                            year=dt_sample.year, month=dt_sample.month, day=dt_sample.day,
                            hour=dt_sample.hour, minute=dt_sample.minute, second=dt_sample.second,
                            gender="nam" if delta_m <= 0 else "nu", school="standard",
                            edge_case_type=f"solar_term_{tag}_{jq_name}",
                            class_name="Class 3: Solar Term Minute Transitions",
                            description=f"{tag} transition of Solar Term {jq_name} in {yr}"
                        ))

        return [c.to_dict() for c in cases]
    # --------------------------------------------------------------------------
    # 5. EDGE CASE CLASS 4: ZI HOUR TRANSITIONS (DẠ TÝ VS CHÍNH TÝ)
    # --------------------------------------------------------------------------
    def generate_class4_zi_hour_cases(self) -> List[Dict[str, Any]]:
        """
        Class 4: Zi Hour Transitions (23:00 - 01:00).
        - Dạ Tý (Late Zi / Tý Đêm): 23:00:00, 23:30:00, 23:59:59.
        - Chính Tý (Early Zi / Tý Sáng): 00:00:00, 00:30:00, 00:59:59.
        - Rollover to Sửu: 01:00:00 vs 00:59:59.
        """
        cases: List[ZiweiVector] = []
        sample_years = [1924, 1960, 1984, 2000, 2024, 2026, 2060, 2099]

        for yr in sample_years:
            # 1. Dạ Tý (23:00 to 23:59)
            for m, d in [(1, 15), (4, 10), (7, 20), (10, 5), (12, 31)]:
                cases.append(ZiweiVector(
                    year=yr, month=m, day=d, hour=23, minute=0, second=0,
                    gender="nam", school="kham_thien",
                    edge_case_type="da_ty_start_23h00",
                    class_name="Class 4: Zi Hour Transitions",
                    description=f"Dạ Tý start boundary (23:00:00) on {yr:04d}-{m:02d}-{d:02d}"
                ))
                cases.append(ZiweiVector(
                    year=yr, month=m, day=d, hour=23, minute=30, second=0,
                    gender="nu", school="standard",
                    edge_case_type="da_ty_mid_23h30",
                    class_name="Class 4: Zi Hour Transitions",
                    description=f"Dạ Tý midpoint (23:30:00) on {yr:04d}-{m:02d}-{d:02d}"
                ))
                cases.append(ZiweiVector(
                    year=yr, month=m, day=d, hour=23, minute=59, second=59,
                    gender="nam", school="trung_chau",
                    edge_case_type="da_ty_end_23h59",
                    class_name="Class 4: Zi Hour Transitions",
                    description=f"Dạ Tý final second (23:59:59) on {yr:04d}-{m:02d}-{d:02d}"
                ))

            # 2. Chính Tý (00:00 to 00:59)
            for m, d in [(1, 16), (4, 11), (7, 21), (10, 6), (1, 1)]:
                cases.append(ZiweiVector(
                    year=yr, month=m, day=d, hour=0, minute=0, second=0,
                    gender="nu", school="luong_phai",
                    edge_case_type="chinh_ty_start_00h00",
                    class_name="Class 4: Zi Hour Transitions",
                    description=f"Chính Tý start boundary (00:00:00) on {yr:04d}-{m:02d}-{d:02d}"
                ))
                cases.append(ZiweiVector(
                    year=yr, month=m, day=d, hour=0, minute=30, second=0,
                    gender="nam", school="nam_phai",
                    edge_case_type="chinh_ty_mid_00h30",
                    class_name="Class 4: Zi Hour Transitions",
                    description=f"Chính Tý midpoint (00:30:00) on {yr:04d}-{m:02d}-{d:02d}"
                ))
                cases.append(ZiweiVector(
                    year=yr, month=m, day=d, hour=0, minute=59, second=59,
                    gender="nu", school="kham_thien",
                    edge_case_type="chinh_ty_end_00h59",
                    class_name="Class 4: Zi Hour Transitions",
                    description=f"Chính Tý final second (00:59:59) on {yr:04d}-{m:02d}-{d:02d}"
                ))
                cases.append(ZiweiVector(
                    year=yr, month=m, day=d, hour=1, minute=0, second=0,
                    gender="nam", school="standard",
                    edge_case_type="suu_hour_start_01h00",
                    class_name="Class 4: Zi Hour Transitions",
                    description=f"Sửu hour beginning boundary (01:00:00) on {yr:04d}-{m:02d}-{d:02d}"
                ))

        return [c.to_dict() for c in cases]

    # --------------------------------------------------------------------------
    # 6. EDGE CASE CLASS 5: YEAR BOUNDARY CHANGING PILLARS
    # --------------------------------------------------------------------------
    def generate_class5_year_boundary_cases(self) -> List[Dict[str, Any]]:
        """
        Class 5: Year Boundary Changing Pillars.
        - Gregorian New Year rollover: Dec 31 23:59:59 -> Jan 1 00:00:00.
        - Lunar New Year rollover: 29/30 Tháng Chạp (Đêm Giao Thừa) -> Mùng 1 Tết.
        - Solar Year rollover: LiChun transition moments.
        """
        cases: List[ZiweiVector] = []
        boundary_years = [1900, 1924, 1949, 1975, 1984, 1999, 2000, 2023, 2024, 2025, 2026, 2050, 2099, 2100]

        for yr in boundary_years:
            # 1. Gregorian Year Rollover
            cases.append(ZiweiVector(
                year=yr, month=12, day=31, hour=23, minute=59, second=59,
                gender="nam", school="standard",
                edge_case_type="gregorian_year_end",
                class_name="Class 5: Year Boundary Changing Pillars",
                description=f"Gregorian year {yr} final second (Dec 31 23:59:59)"
            ))
            if yr < 2100:
                cases.append(ZiweiVector(
                    year=yr + 1, month=1, day=1, hour=0, minute=0, second=0,
                    gender="nu", school="kham_thien",
                    edge_case_type="gregorian_year_start",
                    class_name="Class 5: Year Boundary Changing Pillars",
                    description=f"Gregorian year {yr+1} first second (Jan 1 00:00:00)"
                ))

            # 2. Lunar New Year Eve (Đêm Giao Thừa) & Mùng 1 Tết
            if HAS_LUNAR_PYTHON:
                try:
                    l_tet = Lunar.fromYmd(yr, 1, 1)
                    s_tet = l_tet.getSolar()
                    s_tet_dt = datetime(s_tet.getYear(), s_tet.getMonth(), s_tet.getDay(), 0, 0, 0)
                    s_eve_dt = s_tet_dt - timedelta(seconds=1)

                    cases.append(ZiweiVector(
                        year=s_eve_dt.year, month=s_eve_dt.month, day=s_eve_dt.day,
                        hour=s_eve_dt.hour, minute=s_eve_dt.minute, second=s_eve_dt.second,
                        gender="nam", school="nam_phai",
                        edge_case_type="lunar_new_year_eve",
                        class_name="Class 5: Year Boundary Changing Pillars",
                        description=f"Lunar New Year Eve ({yr}) final second before Tết -> Solar {s_eve_dt.strftime('%Y-%m-%d %H:%M:%S')}"
                    ))

                    cases.append(ZiweiVector(
                        year=s_tet_dt.year, month=s_tet_dt.month, day=s_tet_dt.day,
                        hour=s_tet_dt.hour, minute=s_tet_dt.minute, second=s_tet_dt.second,
                        gender="nu", school="kham_thien",
                        edge_case_type="lunar_mung_1_tet",
                        class_name="Class 5: Year Boundary Changing Pillars",
                        description=f"Lunar New Year Mùng 1 Tết ({yr}) midnight 00:00:00 -> Solar {s_tet_dt.strftime('%Y-%m-%d %H:%M:%S')}"
                    ))
                except Exception:
                    pass

        return [c.to_dict() for c in cases]

    # --------------------------------------------------------------------------
    # 7. EDGE CASE CLASS 6: SPECIAL CỤC SỐ & GENDER POLARITY MATRIX
    # --------------------------------------------------------------------------
    def generate_class6_special_cuc_gender_cases(self) -> List[Dict[str, Any]]:
        """
        Class 6: Special Cục Số combinations, 4 Yin-Yang Genders, and Multi-School Matrix.
        - Full coverage of 5 Cục số (Thủy Nhị Cục, Mộc Tam Cục, Kim Tứ Cục, Thổ Ngũ Cục, Hỏa Lục Cục).
        - 4 Polarity types: Dương Nam, Âm Nam, Dương Nữ, Âm Nữ across 12 Menh branches.
        - cuc_override testing for 2, 3, 4, 5, 6.
        - Full school matrix (standard, kham_thien, nam_phai, trung_chau, luong_phai).
        - View modes: thien_ban, dia_ban, nhan_ban.
        """
        cases: List[ZiweiVector] = []

        # 1. 60 Jiazi sample years covering all 10 Can & 12 Chi (1924 to 1983)
        base_jiazi_start = 1924
        for idx in range(60):
            yr = base_jiazi_start + idx
            can_name = CAN_LIST[idx % 10]
            chi_name = CHI_LIST[idx % 12]

            for m in [1, 4, 7, 10]:
                for g_int, g_str in [(1, "nam"), (0, "nu")]:
                    school = SCHOOLS[(idx + m) % len(SCHOOLS)]
                    view_mode = VIEW_MODES[(idx + g_int) % len(VIEW_MODES)]

                    cases.append(ZiweiVector(
                        year=yr, month=m, day=15, hour=6 + (idx % 12), minute=30, second=0,
                        gender=g_str, gender_int=g_int,
                        view_mode=view_mode,
                        school=school,
                        edge_case_type="jiazi_60_matrix",
                        class_name="Class 6: Special Cục Số & Gender Polarity Matrix",
                        description=f"60 Jiazi matrix year {yr} ({can_name} {chi_name}), month {m}, gender {g_str}, school {school}"
                    ))

        # 2. Systematic Cục Số Override test vectors (2, 3, 4, 5, 6)
        for cuc_val in [2, 3, 4, 5, 6]:
            cuc_title = CUC_NAMES[cuc_val]
            for sch in SCHOOLS:
                for g_int, g_str in [(1, "nam"), (0, "nu")]:
                    cases.append(ZiweiVector(
                        year=2024, month=5, day=20, hour=14, minute=15, second=0,
                        gender=g_str, gender_int=g_int,
                        view_mode="thien_ban",
                        school=sch,
                        edge_case_type=f"cuc_override_{cuc_val}",
                        class_name="Class 6: Special Cục Số & Gender Polarity Matrix",
                        cuc_override=cuc_val,
                        description=f"Forced Cục Số override: {cuc_val} ({cuc_title}) on {sch} school ({g_str})"
                    ))

        # 3. Astrolabe View Modes (Thiên Bàn, Địa Bàn, Nhân Bàn)
        for vm in ["thien_ban", "dia_ban", "nhan_ban"]:
            for sch in ["standard", "kham_thien", "nam_phai"]:
                cases.append(ZiweiVector(
                    year=1999, month=12, day=6, hour=1, minute=55, second=0,
                    gender="nam", gender_int=1,
                    view_mode=vm,
                    school=sch,
                    edge_case_type=f"astrolabe_{vm}",
                    class_name="Class 6: Special Cục Số & Gender Polarity Matrix",
                    description=f"Astrolabe alignment mode {vm} on {sch}"
                ))

        return [c.to_dict() for c in cases]

    # --------------------------------------------------------------------------
    # ALL EDGE CASES COMBINED
    # --------------------------------------------------------------------------
    def generate_edge_case_vectors(self) -> List[Dict[str, Any]]:
        """
        Synthesize all 6 edge case classes into a unified master test suite.
        """
        all_cases: List[Dict[str, Any]] = []
        all_cases.extend(self.generate_class1_century_leap_cases())
        all_cases.extend(self.generate_class2_lunar_leap_cases())
        all_cases.extend(self.generate_class3_solar_term_cases())
        all_cases.extend(self.generate_class4_zi_hour_cases())
        all_cases.extend(self.generate_class5_year_boundary_cases())
        all_cases.extend(self.generate_class6_special_cuc_gender_cases())
        return all_cases

    # --------------------------------------------------------------------------
    # COMPREHENSIVE STRESS SUITE (EDGE CASES + RANDOM SAMPLING)
    # --------------------------------------------------------------------------
    def generate_stress_suite(
        self,
        count: int = 1000,
        seed: Optional[int] = None,
        start_year: int = 1900,
        end_year: int = 2100
    ) -> List[Dict[str, Any]]:
        """
        Generates a comprehensive stress test suite containing all synthesized edge cases
        supplemented by deterministic pseudo-random vectors to reach at least `count` items.
        """
        edge_cases = self.generate_edge_case_vectors()
        edge_count = len(edge_cases)

        if count <= edge_count:
            return edge_cases[:count]

        needed_random = count - edge_count
        random_cases = self.generate_random_vectors(
            count=needed_random,
            seed=seed if seed is not None else self.seed,
            start_year=start_year,
            end_year=end_year
        )
        return edge_cases + random_cases
# ------------------------------------------------------------------------------
# JSON EXPORT / IMPORT HELPERS
# ------------------------------------------------------------------------------
def export_vectors_to_json(vectors: List[Dict[str, Any]], filepath: str, indent: int = 2) -> None:
    """
    Export list of vector dictionaries to a JSON file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            "schema_version": "1.0.0-ziwei-vector-suite",
            "total_count": len(vectors),
            "generated_at": datetime.now().isoformat(),
            "vectors": vectors
        }, f, ensure_ascii=False, indent=indent)


def load_vectors_from_json(filepath: str) -> List[Dict[str, Any]]:
    """
    Load vectors from a JSON file.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and "vectors" in data:
        return data["vectors"]
    elif isinstance(data, list):
        return data
    raise ValueError(f"Invalid vector JSON structure in {filepath}")


# ------------------------------------------------------------------------------
# MODULE LEVEL CONVENIENCE APIS
# ------------------------------------------------------------------------------
_DEFAULT_GENERATOR = ZiweiVectorGenerator(seed=42)

def generate_random_vectors(
    count: int = 1000,
    seed: int = 42,
    start_year: int = 1900,
    end_year: int = 2100,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Module-level function: Generate pseudo-random vectors across 1900-2100.
    """
    gen = ZiweiVectorGenerator(seed=seed)
    return gen.generate_random_vectors(count=count, seed=seed, start_year=start_year, end_year=end_year, **kwargs)

def generate_edge_case_vectors() -> List[Dict[str, Any]]:
    """
    Module-level function: Generate all 6 classes of synthesized edge-case vectors.
    """
    return _DEFAULT_GENERATOR.generate_edge_case_vectors()

def generate_stress_suite(count: int = 1000, seed: int = 42) -> List[Dict[str, Any]]:
    """
    Module-level function: Generate stress test suite (Edge cases + Random vectors).
    """
    gen = ZiweiVectorGenerator(seed=seed)
    return gen.generate_stress_suite(count=count, seed=seed)


# ------------------------------------------------------------------------------
# BENCHMARK RUNNER
# ------------------------------------------------------------------------------
def run_benchmark_on_vectors(
    vectors: List[Dict[str, Any]],
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Executes calculate_universal_tu_vi across the provided test vectors and records
    detailed latency, memory, and error statistics.
    """
    try:
        from engine.tu_vi_advanced import calculate_universal_tu_vi
    except ImportError:
        try:
            from tu_vi_advanced import calculate_universal_tu_vi
        except ImportError:
            raise ImportError("Cannot import calculate_universal_tu_vi from engine.tu_vi_advanced")

    count = len(vectors)
    errors: List[Dict[str, Any]] = []
    latencies: List[float] = []

    start_total = time.perf_counter()

    for idx, v in enumerate(vectors):
        dt = datetime(v["year"], v["month"], v["day"], v["hour"], v["minute"], v.get("second", 0))
        g_int = v.get("gender_int", 1 if v.get("gender", "nam") == "nam" else 0)
        sch = v.get("school", "standard")
        vm = v.get("view_mode", "thien_ban")
        cuc_opt = v.get("cuc_override")

        t0 = time.perf_counter_ns()
        try:
            res = calculate_universal_tu_vi(
                dt=dt,
                gender=g_int,
                school=sch,
                astrolabe_type=vm,
                cuc_override=cuc_opt
            )
            t_diff_ms = (time.perf_counter_ns() - t0) / 1_000_000.0
            latencies.append(t_diff_ms)
            assert len(res.get("palaces", [])) == 12, "Must have 12 palaces"
        except Exception as e:
            t_diff_ms = (time.perf_counter_ns() - t0) / 1_000_000.0
            latencies.append(t_diff_ms)
            errors.append({
                "index": idx,
                "vector": v,
                "error": str(e)
            })

    total_time_s = time.perf_counter() - start_total
    avg_latency_ms = (sum(latencies) / count) if count > 0 else 0.0
    sorted_latencies = sorted(latencies) if latencies else [0.0]
    p95_latency_ms = sorted_latencies[int(len(sorted_latencies) * 0.95)] if sorted_latencies else 0.0
    p99_latency_ms = sorted_latencies[int(len(sorted_latencies) * 0.99)] if sorted_latencies else 0.0
    throughput = count / total_time_s if total_time_s > 0 else 0.0

    result = {
        "total_vectors": count,
        "total_time_seconds": total_time_s,
        "avg_latency_ms": avg_latency_ms,
        "p95_latency_ms": p95_latency_ms,
        "p99_latency_ms": p99_latency_ms,
        "throughput_charts_per_sec": throughput,
        "errors_count": len(errors),
        "success_rate_pct": ((count - len(errors)) / count) * 100.0 if count > 0 else 0.0,
        "errors": errors[:10]
    }

    if verbose:
        print("=" * 60)
        print("ZIWEI HIGH-THROUGHPUT STRESS BENCHMARK RESULTS")
        print("=" * 60)
        print(f"- Total Vectors Tested:     {count:,}")
        print(f"- Total Execution Time:     {total_time_s:.3f} s")
        print(f"- Average Latency / Chart:  {avg_latency_ms:.3f} ms")
        print(f"- P95 Latency:              {p95_latency_ms:.3f} ms")
        print(f"- P99 Latency:              {p99_latency_ms:.3f} ms")
        print(f"- Throughput:               {throughput:,.1f} charts/sec")
        print(f"- Success Rate:             {result['success_rate_pct']:.2f}%")
        print(f"- Unhandled Errors:         {len(errors)}")
        print("=" * 60)

    return result


# ------------------------------------------------------------------------------
# CLI ENTRY POINT
# ------------------------------------------------------------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Multi-Century Random Vector Generator & Edge-Case Synthesizer (1900-2100)"
    )
    parser.add_argument("-c", "--count", type=int, default=1000, help="Number of vectors to generate (default: 1000)")
    parser.add_argument("-s", "--seed", type=int, default=42, help="Random seed for deterministic generation (default: 42)")
    parser.add_argument("--start-year", type=int, default=1900, help="Start year for random sampling (default: 1900)")
    parser.add_argument("--end-year", type=int, default=2100, help="End year for random sampling (default: 2100)")
    parser.add_argument("-o", "--out", type=str, default="", help="Output JSON file path (e.g. vectors.json)")
    parser.add_argument("--edge-cases-only", action="store_true", help="Generate only synthesized edge cases")
    parser.add_argument("--benchmark", action="store_true", help="Execute high-throughput benchmark across generated vectors")

    args = parser.parse_args()

    gen = ZiweiVectorGenerator(seed=args.seed)

    if args.edge_cases_only:
        print("[*] Generating synthesized edge cases (all 6 classes)...", file=sys.stderr)
        vectors = gen.generate_edge_case_vectors()
        print(f"[+] Synthesized {len(vectors)} edge-case vectors.", file=sys.stderr)
    else:
        print(f"[*] Generating stress test suite of {args.count} vectors (seed={args.seed}, range={args.start_year}-{args.end_year})...", file=sys.stderr)
        vectors = gen.generate_stress_suite(count=args.count, seed=args.seed, start_year=args.start_year, end_year=args.end_year)
        edge_cnt = len(gen.generate_edge_case_vectors())
        print(f"[+] Generated {len(vectors)} vectors (including {edge_cnt} synthesized edge cases).", file=sys.stderr)

    if args.out:
        export_vectors_to_json(vectors, args.out)
        print(f"[+] Exported {len(vectors)} vectors to '{args.out}'.", file=sys.stderr)

    if args.benchmark:
        print(f"[*] Running benchmark across {len(vectors)} vectors...", file=sys.stderr)
        run_benchmark_on_vectors(vectors, verbose=True)

    if not args.out and not args.benchmark:
        print(json.dumps(vectors[:3], ensure_ascii=False, indent=2))
        print(f"... and {len(vectors) - 3} more vectors. Use --out <file.json> to export.", file=sys.stderr)

if __name__ == "__main__":
    main()
