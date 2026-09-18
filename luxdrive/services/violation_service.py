import hashlib

class ViolationService:
    VIOLATIONS_DB = [
        {'code': 'CSGT-001', 'type': 'Vượt đèn đỏ', 'fine': '4.000.000 - 6.000.000 đ', 'points': 4, 'icon': '🚦', 'severity': 'high'},
        {'code': 'CSGT-002', 'type': 'Chạy quá tốc độ (20-35km/h)', 'fine': '4.000.000 - 6.000.000 đ', 'points': 2, 'icon': '💨', 'severity': 'high'},
        {'code': 'CSGT-003', 'type': 'Không mang giấy tờ xe', 'fine': '800.000 - 2.000.000 đ', 'points': 0, 'icon': '📄', 'severity': 'medium'},
        {'code': 'CSGT-004', 'type': 'Đi ngược chiều', 'fine': '4.000.000 - 6.000.000 đ', 'points': 4, 'icon': '🔄', 'severity': 'high'},
        {'code': 'CSGT-005', 'type': 'Không thắt dây an toàn', 'fine': '800.000 - 1.000.000 đ', 'points': 0, 'icon': '🔗', 'severity': 'low'},
        {'code': 'CSGT-006', 'type': 'Sử dụng rượu bia khi lái xe', 'fine': '6.000.000 - 8.000.000 đ', 'points': 6, 'icon': '🍺', 'severity': 'critical'},
        {'code': 'CSGT-007', 'type': 'Không có bảo hiểm TNDS', 'fine': '400.000 - 600.000 đ', 'points': 0, 'icon': '🛡️', 'severity': 'medium'},
        {'code': 'CSGT-008', 'type': 'Dừng đỗ sai quy định', 'fine': '800.000 - 2.000.000 đ', 'points': 0, 'icon': '🅿️', 'severity': 'low'},
        {'code': 'CSGT-009', 'type': 'Lấn làn đường', 'fine': '3.000.000 - 5.000.000 đ', 'points': 2, 'icon': '🛤️', 'severity': 'high'},
        {'code': 'CSGT-010', 'type': 'Sử dụng điện thoại khi lái', 'fine': '1.000.000 - 2.000.000 đ', 'points': 0, 'icon': '📱', 'severity': 'medium'},
    ]

    LOCATIONS = [
        'Ngã tư Nguyễn Huệ - Lê Lợi, Q.1, TP.HCM',
        'Cầu Thăng Long, Hà Nội',
        'Đường Phạm Văn Đồng, Thủ Đức, TP.HCM',
        'Quốc lộ 1A, Bình Dương',
        'Đại lộ Võ Văn Kiệt, Q.5, TP.HCM'
    ]

    @classmethod
    def lookup_violation(cls, plate: str) -> dict:
        """Deterministic lookup without random"""
        if not plate or len(plate) < 5:
            return {'found': False, 'message': 'Vui lòng nhập biển số hợp lệ'}
            
        # TODO: Cần kết nối API Cục CSGT thật. Hiện tại dùng Hash biển số để có output cố định.
        hash_val = int(hashlib.md5(plate.encode()).hexdigest(), 16)
        
        # 70% chance of NO violations, 30% chance of 1-3 violations
        if hash_val % 100 < 70:
            return {
                'found': False,
                'plate': plate,
                'message': f'🎉 Xe {plate} không có vi phạm nào! Lái xe an toàn nhé!'
            }
        
        count = (hash_val % 3) + 1
        results = []
        
        for i in range(count):
            v_index = (hash_val + i) % len(cls.VIOLATIONS_DB)
            loc_index = (hash_val + i * 2) % len(cls.LOCATIONS)
            v = cls.VIOLATIONS_DB[v_index].copy()
            
            day = (hash_val % 28) + 1
            month = (hash_val % 12) + 1
            v['date'] = f"{day:02d}/{month:02d}/2024"
            v['location'] = cls.LOCATIONS[loc_index]
            results.append(v)
            
        return {
            'found': True,
            'plate': plate,
            'count': count,
            'violations': results
        }
        
    @classmethod
    def get_common_violations(cls):
        return cls.VIOLATIONS_DB
