class DictionaryService:
    ERRORS_DB = [
        {'code': 'ENG-01', 'name': 'Đèn Cảnh Báo Động Cơ (Check Engine)', 'icon': '⚠️', 'severity': 'High', 'desc': 'Động cơ hoặc hệ thống khí thải gặp sự cố. Cần kiểm tra mã lỗi OBD2 ngay.'},
        {'code': 'BAT-01', 'name': 'Đèn Cảnh Báo Ắc Quy', 'icon': '🔋', 'severity': 'High', 'desc': 'Hệ thống sạc không hoạt động, ắc quy sắp hết điện hoặc máy phát điện hỏng.'},
        {'code': 'OIL-01', 'name': 'Áp Suất Dầu Nhớt Thấp', 'icon': '🛢️', 'severity': 'Critical', 'desc': 'Áp suất dầu bôi trơn quá thấp. Dừng xe ngay lập tức để tránh hỏng động cơ nghiêm trọng.'},
        {'code': 'TPM-01', 'name': 'Áp Suất Lốp Thấp (TPMS)', 'icon': '🛞', 'severity': 'Medium', 'desc': 'Một hoặc nhiều lốp xe đang bị non hơi. Cần bơm lốp để đảm bảo an toàn và tiết kiệm nhiên liệu.'},
        {'code': 'ABS-01', 'name': 'Lỗi Hệ Thống Phanh ABS', 'icon': '🛑', 'severity': 'High', 'desc': 'Hệ thống chống bó cứng phanh không hoạt động. Phanh cơ bản vẫn hoạt động nhưng kém an toàn khi phanh gấp.'},
        {'code': 'TMP-01', 'name': 'Nhiệt Độ Nước Làm Mát Cao', 'icon': '🌡️', 'severity': 'Critical', 'desc': 'Động cơ đang quá nhiệt (sôi nước). Dừng xe ngay lập tức, tắt máy và đợi nguội.'},
        {'code': 'AIR-01', 'name': 'Lỗi Túi Khí (Airbag)', 'icon': '🎈', 'severity': 'High', 'desc': 'Hệ thống túi khí có lỗi và có thể không bung khi xảy ra va chạm.'},
        {'code': 'WSH-01', 'name': 'Hết Nước Rửa Kính', 'icon': '💦', 'severity': 'Low', 'desc': 'Bình nước rửa kính đã cạn, cần châm thêm.'},
    ]

    @classmethod
    def search_errors(cls, search_term: str) -> list:
        # TODO: Đưa data vào CSDL và query bằng SQL ILIKE
        search = search_term.lower()
        if not search:
            return cls.ERRORS_DB
        
        return [e for e in cls.ERRORS_DB if search in e['name'].lower() or search in e['code'].lower() or search in e['desc'].lower()]
