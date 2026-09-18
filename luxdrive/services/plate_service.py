import random

class PlateService:
    @staticmethod
    def analyze_plate(plate_number: str) -> dict:
        """Hàm phân tích biển số chung"""
        # Xóa ký tự không phải số ở phần đuôi
        parts = plate_number.replace('.', '').replace('-', '').split()
        tail = parts[-1] if len(parts) > 0 else plate_number
        digits_only = ''.join([c for c in tail if c.isdigit()])
        
        if not digits_only:
            digits_only = str(random.randint(10000, 99999))

        # Định giá cơ bản
        base_value = 2_000_000
        multiplier = 1.0
        meaning = "Biển số bình thường, mang ý nghĩa an toàn, bình an."
        tags = []

        # Heuristics
        if len(digits_only) >= 5:
            if digits_only == digits_only[0] * len(digits_only): # Ngũ quý
                multiplier = 500.0
                meaning = "Ngũ quý đại cát, mang lại quyền lực và tài lộc vượng phát."
                tags.append("Ngũ Quý")
            elif digits_only in ['12345', '56789', '34567']: # Sảnh tiến
                multiplier = 200.0
                meaning = "Sảnh tiến vạn dặm, công danh sự nghiệp không ngừng thăng tiến."
                tags.append("Sảnh Tiến")
            elif digits_only[-4:] == digits_only[-4]: # Tứ quý đuôi
                multiplier = 100.0
                meaning = "Tứ quý phú quý, gia đạo êm ấm, tài lộc dồi dào."
                tags.append("Tứ Quý")
        
        if '68' in digits_only or '86' in digits_only:
            multiplier += 5.0
            if "Lộc Phát" not in meaning:
                meaning = "Chứa cặp số Lộc Phát (68/86), rất tốt cho việc làm ăn kinh doanh."
            tags.append("Lộc Phát")
        
        if '39' in digits_only or '79' in digits_only:
            multiplier += 3.0
            tags.append("Thần Tài")
        
        if '49' in digits_only or '53' in digits_only:
            multiplier *= 0.5
            tags.append("Kém May Mắn")
        
        if '4' in digits_only:
            multiplier *= 0.8
            
        value = int(base_value * multiplier)
        
        # Phong thủy
        total_sum = sum(int(d) for d in digits_only)
        nut = total_sum % 10
        if nut == 0: nut = 10
        
        last_digit = int(digits_only[-1])
        element_map = {1: 'Thủy', 2: 'Thổ', 3: 'Mộc', 4: 'Mộc', 5: 'Thổ', 6: 'Kim', 7: 'Kim', 8: 'Thổ', 9: 'Hỏa', 0: 'Thủy'}
        element = element_map.get(last_digit, 'Kim')

        return {
            'plate': plate_number,
            'digits': digits_only,
            'value': value,
            'value_formatted': f"{value:,}".replace(',', '.') + " đ",
            'meaning': meaning,
            'tags': tags,
            'nut': nut,
            'element': element
        }
