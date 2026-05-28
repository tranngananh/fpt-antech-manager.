import json
import os

# ==========================================
# CẤU HÌNH ĐƯỜNG DẪN FILE DỮ LIỆU
# ==========================================
DATA_DIR = './data'
NGUOI_HOC_FILE = os.path.join(DATA_DIR, 'nguoi_hoc.json')
DIEM_DANH_FILE = os.path.join(DATA_DIR, 'diem_danh.json')

# ==========================================
# LÕI XỬ LÝ ĐỌC / GHI FILE JSON (DATA ENGINE)
# ==========================================
class DataEngine:
    @staticmethod
    def initialize_db():
        """
        Kiểm tra xem thư mục data và các file JSON đã tồn tại chưa.
        Nếu chưa có, tự động tạo mới file rỗng.
        """
        os.makedirs(DATA_DIR, exist_ok=True)
        
        for filepath in [NGUOI_HOC_FILE, DIEM_DANH_FILE]:
            if not os.path.exists(filepath) or os.stat(filepath).st_size == 0:
                # File điểm danh là Dictionary {}, file người học là List []
                default = {} if filepath == DIEM_DANH_FILE else []
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(default, f, indent=4, ensure_ascii=False)
        print("✅ Đã kiểm tra và khởi tạo hệ thống cơ sở dữ liệu thành công!")

    @staticmethod
    def read_file(filepath):
        """Đọc dữ liệu từ file JSON được chỉ định"""
        if not os.path.exists(filepath):
            return {} if filepath == DIEM_DANH_FILE else []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {} if filepath == DIEM_DANH_FILE else []

    @staticmethod
    def write_file(filepath, data):
        """Ghi dữ liệu xuống file JSON được chỉ định"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)