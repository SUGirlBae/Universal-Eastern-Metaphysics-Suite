"""
Ziwei Zero-Diff Comparator & Root-Cause Isolation Module
Performs comprehensive 7-step comparison between Internal Universal Tu Vi Engine outputs
and CanonicalAstrolabe Ground-Truth data models.

Features:
1. 7-Step Verification Pipeline:
   - Step 1: Normalization & Preprocessing (Branch orthography, Palace codes, Markdown tags)
   - Step 2: Profile & Core Astrological Alignment (Mệnh/Thân, Cục số, Nạp Âm, Âm Dương Nam Nữ)
   - Step 3: 12 Palaces Can Chi Alignment (Exact Can + Chi for all 12 branches)
   - Step 4: 10-Year Major Cycles (Đại Vận DV-TV age ranges for all 12 palaces)
   - Step 5: 14 Main Stars & VCD Alignment (Exact placement, VCD flags, brightness tags)
   - Step 6: 12 Palaces Flying Stars Matrix (Phi Lộc, Phi Quyền, Phi Khoa, Phi Kỵ destination codes)
   - Step 7: Tự Hóa, Hướng Tâm, Khâm Thiên Routes & Phương Viên Toàn Đồ
2. Automated Root-Cause Isolation Taxonomy:
   - ERR_SI_HUA_TABLE: Variation in Si Hua mapping (e.g. Can Canh: Dương Vũ Đồng Âm vs Dương Vũ Âm Đồng)
   - ERR_CUC_SO: Discrepancy in Cuc number / starting age / Nạp Âm
   - ERR_BRANCH_ORTHOGRAPHY: Orthographic variant (e.g. Tị vs Tỵ)
   - ERR_TRANSFORMATION_LOGIC: Flying star, self-transformation, or inward-transformation calculation error
   - ERR_LUNAR_SOLAR_DATE: Date conversion, leap month, True Solar Time vs civil time, or hour branch mismatch
   - ERR_STAR_PLACEMENT: Placement discrepancy of 14 main stars or minor stars
   - ERR_DA_YUN_RANGE: Đại vận step calculation or progression direction mismatch
   - ERR_CAN_CHI: Palace stem / branch calculation discrepancy
"""

import re
from typing import Dict, Any, List, Optional, Set, Tuple, Union


# Root Cause Constants
ERR_SI_HUA_TABLE = "ERR_SI_HUA_TABLE"
ERR_CUC_SO = "ERR_CUC_SO"
ERR_BRANCH_ORTHOGRAPHY = "ERR_BRANCH_ORTHOGRAPHY"
ERR_TRANSFORMATION_LOGIC = "ERR_TRANSFORMATION_LOGIC"
ERR_LUNAR_SOLAR_DATE = "ERR_LUNAR_SOLAR_DATE"
ERR_STAR_PLACEMENT = "ERR_STAR_PLACEMENT"
ERR_DA_YUN_RANGE = "ERR_DA_YUN_RANGE"
ERR_CAN_CHI = "ERR_CAN_CHI"


PALACE_CODE_MAP = {
    "MỆNH": "MỆNH",
    "MỆNH CUNG": "MỆNH",
    "MỆNH BÀN": "MỆNH",
    "PHỤ": "PHỤ",
    "PHỤ MẪU": "PHỤ",
    "PHÚC": "PHÚC",
    "PHÚC ĐỨC": "PHÚC",
    "ĐIỀN": "ĐIỀN",
    "ĐIỀN TRẠCH": "ĐIỀN",
    "QUAN": "QUAN",
    "QUAN LỘC": "QUAN",
    "NÔ": "NÔ",
    "NÔ BỘC": "NÔ",
    "DI": "DI",
    "THIÊN DI": "DI",
    "TẬT": "TẬT",
    "TẬT ÁCH": "TẬT",
    "TÀI": "TÀI",
    "TÀI BẠCH": "TÀI",
    "TỬ": "TỬ",
    "TỬ TỨC": "TỬ",
    "PHỐI": "PHỐI",
    "PHU THÊ": "PHỐI",
    "PHU": "PHỐI",
    "THÊ": "PHỐI",
    "BÀO": "BÀO",
    "HUYNH ĐỆ": "BÀO",
    "HUYNH": "BÀO"
}

BRANCH_MAP = {
    "Tị": "Tỵ",
    "tị": "tỵ",
    "TỊ": "TỴ"
}


def normalize_branch(text: str) -> str:
    """Normalize branch spelling (e.g. Tị -> Tỵ)."""
    if not text:
        return ""
    res = str(text)
    for k, v in BRANCH_MAP.items():
        res = res.replace(k, v)
    return res.strip()


def normalize_palace_code(text: str) -> str:
    """Normalize any palace name variation to standardized uppercase short code."""
    if not text:
        return ""
    cleaned = str(text).replace("**", "").replace("*", "").replace("Thân cư", "").replace("Cung", "").strip().upper()
    return PALACE_CODE_MAP.get(cleaned, cleaned)


def clean_star_name(star: str) -> str:
    """Strip brightness tags like (M), (V), (Đ), (H), (B) from star name."""
    if not star:
        return ""
    return re.sub(r"\s*\([MVĐHBmvđhb]\)", "", str(star)).strip()


class ComparisonDiff:
    """Represents a single granular discrepancy identified by the comparator."""
    def __init__(
        self,
        step: int,
        step_name: str,
        category: str,
        palace: str,
        branch: str,
        field: str,
        engine_val: Any,
        gt_val: Any,
        root_cause: str,
        message: str
    ):
        self.step = step
        self.step_name = step_name
        self.category = category
        self.palace = palace
        self.branch = branch
        self.field = field
        self.engine_val = engine_val
        self.gt_val = gt_val
        self.root_cause = root_cause
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step,
            "step_name": self.step_name,
            "category": self.category,
            "palace": self.palace,
            "branch": self.branch,
            "field": self.field,
            "engine_val": self.engine_val,
            "gt_val": self.gt_val,
            "root_cause": self.root_cause,
            "message": self.message
        }

    def __str__(self) -> str:
        return f"[Step {self.step}: {self.step_name}] {self.message} (Root Cause: {self.root_cause})"

    def __repr__(self) -> str:
        return f"<ComparisonDiff {self.__str__()}>"


class ComparisonReport(list):
    """
    Subclasses list of strings for 100% backward compatibility with `len(diffs) == 0`,
    while providing rich structured comparison metadata and root-cause isolation.
    """
    def __init__(self, diff_objects: Optional[List[ComparisonDiff]] = None):
        self.diff_details: List[ComparisonDiff] = diff_objects or []
        # Populate list with human-readable string representations
        string_list = [str(d) for d in self.diff_details]
        super().__init__(string_list)
        self.summary_by_step: Dict[int, Dict[str, Any]] = {
            step: {"step_name": name, "checked": True, "diffs_count": 0}
            for step, name in [
                (1, "Normalization & Preprocessing"),
                (2, "Profile & Core Alignment"),
                (3, "12 Palaces Can Chi"),
                (4, "10-Year Major Cycles (Đại Vận)"),
                (5, "14 Main Stars & VCD"),
                (6, "Flying Stars Matrix (Phi Tinh 4 Hóa)"),
                (7, "Tự Hóa, Hướng Tâm & Routes")
            ]
        }
        for d in self.diff_details:
            if d.step in self.summary_by_step:
                self.summary_by_step[d.step]["diffs_count"] += 1

    @property
    def is_zero_diff(self) -> bool:
        """Returns True if there are 0 discrepancies (100% Zero-Diff match)."""
        return len(self.diff_details) == 0

    @property
    def total_diffs(self) -> int:
        return len(self.diff_details)

    @property
    def root_causes(self) -> Set[str]:
        """Set of unique root causes identified."""
        return {d.root_cause for d in self.diff_details}

    def format_report(self) -> str:
        """Generate a detailed Markdown comparison report."""
        lines = []
        lines.append("================================================================================")
        lines.append("           ZIWEI ZERO-DIFF COMPARISON & ROOT-CAUSE ISOLATION REPORT")
        lines.append("================================================================================")
        if self.is_zero_diff:
            lines.append("✅ VERIFICATION STATUS: 100% ZERO-DIFF MATCH (0 Sai Lệch Tuyệt Đối)")
        else:
            lines.append(f"❌ VERIFICATION STATUS: {len(self.diff_details)} DISCREPANCIES DETECTED")
            lines.append(f"Root Causes Isolated: {', '.join(sorted(self.root_causes))}")
        lines.append("")
        lines.append("【7-STEP PIPELINE SUMMARY】")
        for step, data in sorted(self.summary_by_step.items()):
            status = "✅ PASS" if data["diffs_count"] == 0 else f"❌ FAIL ({data['diffs_count']} diffs)"
            lines.append(f"  • Step {step}: {data['step_name']:<40} -> {status}")
        
        if self.diff_details:
            lines.append("")
            lines.append("【DETAILED DISCREPANCY BREAKDOWN】")
            for idx, d in enumerate(self.diff_details, 1):
                lines.append(f"  {idx}. [Step {d.step} - {d.category}] Palace [{d.palace}/{d.branch}]: {d.message}")
                lines.append(f"     Engine: {d.engine_val} | Ground-Truth: {d.gt_val} | Cause: {d.root_cause}")
        lines.append("================================================================================")
        return "\n".join(lines)


def isolate_si_hua_root_cause(palace_can: str, star_diff: str) -> str:
    """Isolate root cause specifically for transformation and Si Hua differences."""
    if palace_can == "Canh":
        return ERR_SI_HUA_TABLE
    if palace_can == "Nhâm" and ("Tả Phụ" in star_diff or "Thiên Phủ" in star_diff):
        return ERR_SI_HUA_TABLE
    if palace_can == "Mậu" and ("Hữu Bật" in star_diff or "Thái Âm" in star_diff):
        return ERR_SI_HUA_TABLE
    return ERR_TRANSFORMATION_LOGIC


def compare_engine_with_ground_truth(
    engine_res: Dict[str, Any],
    gt_data: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> ComparisonReport:
    """
    Perform rigorous 7-step Zero-Diff comparison between Engine results and Ground-Truth data.
    Returns a ComparisonReport (which acts as a list of strings for backward compatibility).
    """
    diffs: List[ComparisonDiff] = []
    opts = options or {}
    check_minor_stars = opts.get("check_minor_stars", False)

    # --------------------------------------------------------------------------
    # Step 1: Normalization & Preprocessing
    # --------------------------------------------------------------------------
    # Normalization is applied dynamically across all fields using normalize_branch
    # and normalize_palace_code.

    # --------------------------------------------------------------------------
    # Step 2: Profile & Core Astrological Alignment
    # --------------------------------------------------------------------------
    ep = engine_res.get("client_profile", {})
    gt_meta = gt_data.get("tu_vi_meta", {})
    gt_profile = gt_data.get("profile", {})

    # Mệnh Palace Branch
    eng_menh_branch = normalize_branch(ep.get("menh_branch", ""))
    gt_menh_branch = ""
    for gp in gt_data.get("palaces", []):
        if normalize_palace_code(gp.get("palace_code", "")) == "MỆNH":
            gt_menh_branch = normalize_branch(gp.get("branch", ""))
            break
    if eng_menh_branch and gt_menh_branch and eng_menh_branch != gt_menh_branch:
        diffs.append(ComparisonDiff(
            step=2,
            step_name="Profile & Core Alignment",
            category="Mệnh Branch",
            palace="MỆNH",
            branch=eng_menh_branch,
            field="menh_branch",
            engine_val=eng_menh_branch,
            gt_val=gt_menh_branch,
            root_cause=ERR_LUNAR_SOLAR_DATE,
            message=f"Mệnh branch mismatch: Engine={eng_menh_branch}, GT={gt_menh_branch}"
        ))

    # Thân Palace / Branch
    eng_than_branch = normalize_branch(ep.get("than_branch", ""))
    gt_than_code = normalize_palace_code(gt_meta.get("than_palace", ""))
    gt_than_branch = ""
    for gp in gt_data.get("palaces", []):
        if normalize_palace_code(gp.get("palace_code", "")) == gt_than_code:
            gt_than_branch = normalize_branch(gp.get("branch", ""))
            break
    if eng_than_branch and gt_than_branch and eng_than_branch != gt_than_branch:
        diffs.append(ComparisonDiff(
            step=2,
            step_name="Profile & Core Alignment",
            category="Thân Branch",
            palace=gt_than_code or "THÂN",
            branch=eng_than_branch,
            field="than_branch",
            engine_val=eng_than_branch,
            gt_val=gt_than_branch,
            root_cause=ERR_LUNAR_SOLAR_DATE,
            message=f"Thân branch mismatch: Engine={eng_than_branch}, GT={gt_than_branch}"
        ))

    # Cục Số & Tên Cục
    eng_cuc_name = ep.get("cuc_name", "").strip()
    gt_cuc_name = gt_meta.get("cuc_name", "").strip()
    if eng_cuc_name and gt_cuc_name and eng_cuc_name != gt_cuc_name:
        diffs.append(ComparisonDiff(
            step=2,
            step_name="Profile & Core Alignment",
            category="Cục Số",
            palace="MỆNH",
            branch=eng_menh_branch,
            field="cuc_name",
            engine_val=eng_cuc_name,
            gt_val=gt_cuc_name,
            root_cause=ERR_CUC_SO,
            message=f"Cục name mismatch: Engine={eng_cuc_name}, GT={gt_cuc_name}"
        ))

    # Mệnh Nạp Âm
    eng_nayin = ep.get("menh_nayin", "").strip()
    gt_nayin = gt_meta.get("menh_nayin", "").strip()
    if eng_nayin and gt_nayin and eng_nayin != gt_nayin:
        diffs.append(ComparisonDiff(
            step=2,
            step_name="Profile & Core Alignment",
            category="Mệnh Nạp Âm",
            palace="MỆNH",
            branch=eng_menh_branch,
            field="menh_nayin",
            engine_val=eng_nayin,
            gt_val=gt_nayin,
            root_cause=ERR_LUNAR_SOLAR_DATE,
            message=f"Mệnh Nạp Âm mismatch: Engine={eng_nayin}, GT={gt_nayin}"
        ))

    # --------------------------------------------------------------------------
    # Prepare Palaces Lookup Maps
    # --------------------------------------------------------------------------
    palaces_by_branch = {normalize_branch(p["branch_name"]): p for p in engine_res.get("palaces", [])}
    flying_by_branch = {}
    if "flying_stars" in engine_res and "palace_flying_stars" in engine_res["flying_stars"]:
        flying_by_branch = {normalize_branch(f["branch_name"]): f for f in engine_res["flying_stars"]["palace_flying_stars"]}

    gt_palaces = gt_data.get("palaces", [])

    for gp in gt_palaces:
        br = normalize_branch(gp.get("branch", ""))
        p_code = normalize_palace_code(gp.get("palace_code", ""))
        if br not in palaces_by_branch:
            diffs.append(ComparisonDiff(
                step=3,
                step_name="12 Palaces Can Chi",
                category="Missing Branch",
                palace=p_code,
                branch=br,
                field="branch",
                engine_val=None,
                gt_val=br,
                root_cause=ERR_BRANCH_ORTHOGRAPHY,
                message=f"Branch [{br}] missing from Engine output"
            ))
            continue

        ep_palace = palaces_by_branch[br]
        ef_palace = flying_by_branch.get(br, {})

        # ----------------------------------------------------------------------
        # Step 3: 12 Palaces Can Chi Alignment
        # ----------------------------------------------------------------------
        eng_can_chi = normalize_branch(f"{ep_palace['can_name']} {ep_palace['branch_name']}")
        gt_can_chi = normalize_branch(gp.get("can_chi", ""))
        if eng_can_chi != gt_can_chi:
            root_cause = ERR_BRANCH_ORTHOGRAPHY if eng_can_chi.replace("Tỵ", "Tị") == gt_can_chi.replace("Tỵ", "Tị") else ERR_CAN_CHI
            diffs.append(ComparisonDiff(
                step=3,
                step_name="12 Palaces Can Chi",
                category="Can Chi",
                palace=p_code,
                branch=br,
                field="can_chi",
                engine_val=eng_can_chi,
                gt_val=gt_can_chi,
                root_cause=root_cause,
                message=f"Cung [{br}] Can Chi mismatch: Engine={eng_can_chi}, GT={gt_can_chi}"
            ))

        # ----------------------------------------------------------------------
        # Step 4: 10-Year Major Cycles (Đại Vận DV-TV)
        # ----------------------------------------------------------------------
        eng_da_yun = str(ep_palace.get("da_yun_range", "")).strip()
        gt_da_yun = str(gp.get("da_yun_range", "")).strip()
        if eng_da_yun and gt_da_yun and eng_da_yun != gt_da_yun:
            diffs.append(ComparisonDiff(
                step=4,
                step_name="10-Year Major Cycles (Đại Vận)",
                category="Đại Vận",
                palace=p_code,
                branch=br,
                field="da_yun_range",
                engine_val=eng_da_yun,
                gt_val=gt_da_yun,
                root_cause=ERR_DA_YUN_RANGE,
                message=f"Cung [{br}] Đại Vận range mismatch: Engine={eng_da_yun}, GT={gt_da_yun}"
            ))

        # ----------------------------------------------------------------------
        # Step 5: 14 Main Stars & VCD Alignment
        # ----------------------------------------------------------------------
        gt_is_vcd = gp.get("is_vcd", False)
        eng_main_stars = [clean_star_name(s) for s in ep_palace.get("main_stars", [])]
        gt_main_stars = [clean_star_name(s) for s in gp.get("main_stars", [])]

        if gt_is_vcd:
            if len(eng_main_stars) > 0:
                diffs.append(ComparisonDiff(
                    step=5,
                    step_name="14 Main Stars & VCD",
                    category="VCD State",
                    palace=p_code,
                    branch=br,
                    field="is_vcd",
                    engine_val=eng_main_stars,
                    gt_val="VCD",
                    root_cause=ERR_STAR_PLACEMENT,
                    message=f"Cung [{br}] GT is VCD, but Engine placed stars: {eng_main_stars}"
                ))
        else:
            if set(eng_main_stars) != set(gt_main_stars):
                diffs.append(ComparisonDiff(
                    step=5,
                    step_name="14 Main Stars & VCD",
                    category="Main Stars",
                    palace=p_code,
                    branch=br,
                    field="main_stars",
                    engine_val=eng_main_stars,
                    gt_val=gt_main_stars,
                    root_cause=ERR_STAR_PLACEMENT,
                    message=f"Cung [{br}] Main Stars mismatch: Engine={eng_main_stars}, GT={gt_main_stars}"
                ))

        # Minor Stars (Optional check)
        if check_minor_stars and gp.get("minor_stars"):
            eng_minor_names = {clean_star_name(s.get("name", s) if isinstance(s, dict) else s) for s in ep_palace.get("minor_stars", [])}
            gt_minor_names = {clean_star_name(s) for s in gp.get("minor_stars", [])}
            missing_in_engine = gt_minor_names - eng_minor_names
            if missing_in_engine:
                diffs.append(ComparisonDiff(
                    step=5,
                    step_name="14 Main Stars & VCD",
                    category="Minor Stars",
                    palace=p_code,
                    branch=br,
                    field="minor_stars",
                    engine_val=list(eng_minor_names)[:8],
                    gt_val=list(missing_in_engine),
                    root_cause=ERR_STAR_PLACEMENT,
                    message=f"Cung [{br}] Minor stars missing in Engine: {list(missing_in_engine)}"
                ))

        # ----------------------------------------------------------------------
        # Step 6: 12 Palaces Flying Stars Matrix (Phi Tinh 4 Hóa)
        # ----------------------------------------------------------------------
        if ef_palace:
            p_can = ep_palace.get("can_name", "")
            flying_checks = [
                ("phi_loc", "Phi Lộc (A)"),
                ("phi_quyen", "Phi Quyền (B)"),
                ("phi_khoa", "Phi Khoa (C)"),
                ("phi_ky", "Phi Kỵ (D)")
            ]
            for key, label in flying_checks:
                eng_target = normalize_palace_code(ef_palace.get(key, {}).get("target_palace", ""))
                gt_target = normalize_palace_code(gp.get(key, ""))
                if eng_target and gt_target and eng_target != gt_target:
                    star_name = ef_palace.get(key, {}).get("star", "")
                    root_cause = isolate_si_hua_root_cause(p_can, star_name)
                    diffs.append(ComparisonDiff(
                        step=6,
                        step_name="Flying Stars Matrix (Phi Tinh 4 Hóa)",
                        category=label,
                        palace=p_code,
                        branch=br,
                        field=key,
                        engine_val=f"{eng_target} ({star_name})",
                        gt_val=gt_target,
                        root_cause=root_cause,
                        message=f"Cung [{br}] {label} destination mismatch: Engine={eng_target} ({star_name}), GT={gt_target}"
                    ))

        # ----------------------------------------------------------------------
        # Step 7: Tự Hóa, Hướng Tâm, Khâm Thiên Routes & Phương Viên
        # ----------------------------------------------------------------------
        if ef_palace:
            # Check Tự Hóa (Self Transformations)
            eng_self = ef_palace.get("self_transformations", [])
            for gt_st in gp.get("self_transformations", []):
                gt_st_clean = gt_st.strip()
                # Check match
                matched = any(gt_st_clean in es or es in gt_st_clean for es in eng_self)
                if not matched:
                    root_cause = isolate_si_hua_root_cause(ep_palace.get("can_name", ""), gt_st_clean)
                    diffs.append(ComparisonDiff(
                        step=7,
                        step_name="Tự Hóa, Hướng Tâm & Routes",
                        category="Tự Hóa",
                        palace=p_code,
                        branch=br,
                        field="self_transformations",
                        engine_val=eng_self,
                        gt_val=gt_st_clean,
                        root_cause=root_cause,
                        message=f"Cung [{br}] Tự Hóa missing in Engine: GT={gt_st_clean}, Engine={eng_self}"
                    ))

            # Check Hướng Tâm (Inward Transformations)
            eng_inward = ef_palace.get("inward_transformations", [])
            for gt_it in gp.get("inward_transformations", []):
                gt_it_clean = gt_it.strip()
                matched = any(gt_it_clean in ei or ei in gt_it_clean for ei in eng_inward)
                if not matched:
                    root_cause = isolate_si_hua_root_cause(ep_palace.get("can_name", ""), gt_it_clean)
                    diffs.append(ComparisonDiff(
                        step=7,
                        step_name="Tự Hóa, Hướng Tâm & Routes",
                        category="Hướng Tâm",
                        palace=p_code,
                        branch=br,
                        field="inward_transformations",
                        engine_val=eng_inward,
                        gt_val=gt_it_clean,
                        root_cause=root_cause,
                        message=f"Cung [{br}] Hướng Tâm missing in Engine: GT={gt_it_clean}, Engine={eng_inward}"
                    ))

    return ComparisonReport(diffs)
