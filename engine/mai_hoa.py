"""
Mai Hoa Dich So (Plum Blossom Divination Engine)
Calculates Upper, Lower, Moving Line, Primary, Mutual, and Transformed Hexagrams.
"""

try:
    from .lunar_solar import calculate_time_coordinates, CHI
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, CHI

# 8 Trigrams (Bát Quái Tiên Thiên)
# 1: Càn (111), 2: Đoài (011), 3: Ly (101), 4: Chấn (001), 5: Tốn (110), 6: Khảm (010), 7: Cấn (100), 8: Khôn (000)
# (1 = Dương, 0 = Âm, tính từ hào 1 dưới lên hào 3 trên)
TRIGRAMS = {
    1: {"name": "Càn", "symbol": "Thiên", "element": "Kim", "lines": [1, 1, 1], "han": "乾"},
    2: {"name": "Đoài", "symbol": "Trạch", "element": "Kim", "lines": [1, 1, 0], "han": "兌"},
    3: {"name": "Ly", "symbol": "Hỏa", "element": "Hỏa", "lines": [1, 0, 1], "han": "離"},
    4: {"name": "Chấn", "symbol": "Lôi", "element": "Mộc", "lines": [1, 0, 0], "han": "震"},
    5: {"name": "Tốn", "symbol": "Phong", "element": "Mộc", "lines": [0, 1, 1], "han": "巽"},
    6: {"name": "Khảm", "symbol": "Thủy", "element": "Thủy", "lines": [0, 1, 0], "han": "坎"},
    7: {"name": "Cấn", "symbol": "Sơn", "element": "Thổ", "lines": [0, 0, 1], "han": "艮"},
    8: {"name": "Khôn", "symbol": "Địa", "element": "Thổ", "lines": [0, 0, 0], "han": "坤"}
}

# Mapping Lines to Trigram ID (lines: [bottom, middle, top])
LINES_TO_TRIGRAM = {
    (1, 1, 1): 1, # Càn
    (1, 1, 0): 2, # Đoài
    (1, 0, 1): 3, # Ly
    (1, 0, 0): 4, # Chấn
    (0, 1, 1): 5, # Tốn
    (0, 1, 0): 6, # Khảm
    (0, 0, 1): 7, # Cấn
    (0, 0, 0): 8  # Khôn
}

def get_trigram_from_num(num):
    val = num % 8
    return 8 if val == 0 else val

def get_moving_line_from_num(num):
    val = num % 6
    return 6 if val == 0 else val

def calculate_mai_hoa_from_time(time_coords):
    # Chi index (Tý=1, Sửu=2, ..., Hợi=12)
    year_chi_idx = CHI.index(time_coords["year_chi"]) + 1
    month_num = time_coords["lunar_month"]
    day_num = time_coords["lunar_day"]
    hour_chi_idx = CHI.index(time_coords["hour_chi"]) + 1
    
    # Mai Hoa Formula
    upper_num = get_trigram_from_num(year_chi_idx + month_num + day_num)
    lower_num = get_trigram_from_num(year_chi_idx + month_num + day_num + hour_chi_idx)
    moving_line = get_moving_line_from_num(year_chi_idx + month_num + day_num + hour_chi_idx)
    
    return build_hexagram_system(upper_num, lower_num, moving_line)

def build_hexagram_system(upper_id, lower_id, moving_line):
    upper_tri = TRIGRAMS[upper_id]
    lower_tri = TRIGRAMS[lower_id]
    
    # 6 lines of primary hexagram (index 0 = Line 1 [bottom], index 5 = Line 6 [top])
    primary_lines = lower_tri["lines"] + upper_tri["lines"]
    
    # Transformed hexagram (Quẻ Biến): Flip moving line (1-indexed)
    transformed_lines = list(primary_lines)
    transformed_lines[moving_line - 1] = 1 - transformed_lines[moving_line - 1]
    
    trans_lower_id = LINES_TO_TRIGRAM[tuple(transformed_lines[0:3])]
    trans_upper_id = LINES_TO_TRIGRAM[tuple(transformed_lines[3:6])]
    
    # Mutual hexagram (Quẻ Hỗ): Lines 2,3,4 as lower; Lines 3,4,5 as upper
    mutual_lower_lines = [primary_lines[1], primary_lines[2], primary_lines[3]]
    mutual_upper_lines = [primary_lines[2], primary_lines[3], primary_lines[4]]
    
    mutual_lower_id = LINES_TO_TRIGRAM[tuple(mutual_lower_lines)]
    mutual_upper_id = LINES_TO_TRIGRAM[tuple(mutual_upper_lines)]
    
    # Determine Thể / Dụng: The trigram containing moving line is Dụng, the other is Thể
    if moving_line <= 3:
        the_quai = upper_tri
        dung_quai = lower_tri
        the_position = "Thượng (Ngoại)"
        dung_position = "Hạ (Nội)"
    else:
        the_quai = lower_tri
        dung_quai = upper_tri
        the_position = "Hạ (Nội)"
        dung_position = "Thượng (Ngoại)"
        
    return {
        "upper_id": upper_id,
        "lower_id": lower_id,
        "moving_line": moving_line,
        "primary_lines": primary_lines,
        "transformed_lines": transformed_lines,
        "mutual_lower_id": mutual_lower_id,
        "mutual_upper_id": mutual_upper_id,
        "trans_lower_id": trans_lower_id,
        "trans_upper_id": trans_upper_id,
        "the_quai": the_quai,
        "dung_quai": dung_quai,
        "the_position": the_position,
        "dung_position": dung_position
    }
