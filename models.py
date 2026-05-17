# models.py
import json
import os
import re
from config import Config

class DataEngine:
    @staticmethod
    def initialize_db():
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        if not os.path.exists(Config.NGUOI_HOC_FILE) or os.stat(Config.NGUOI_HOC_FILE).st_size == 0:
            with open(Config.NGUOI_HOC_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    @staticmethod
    def read_file():
        if not os.path.exists(Config.NGUOI_HOC_FILE):
            return []
        with open(Config.NGUOI_HOC_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
            
        result = []
        
        for s in data:
            # Khởi tạo khung dữ liệu chuẩn cho giao diện HTML đọc
            target = {
                'id': '-',
                'ho_va_ten': '-',
                'so_dien_thoai': '-',
                'dan_toc': 'Kinh',
                'gioi_tinh': 'Nam',
                'ngay_sinh': '-',
                'email': '-',
                'dia_chi': '-',
                'khoa_hoc': 'full-stack',
                'diem_danh': 0,
                'canh_bao': 'Không'
            }
            
            # 🌟 BỘ QUÉT TỪ KHÓA THÔNG MINH: Tìm kiếm từ khóa chứa trong Key để bọc lót mọi lỗi định dạng
            for k, v in s.items():
                k_low = str(k).lower().strip()
            # Khớp Mã ID (Chỉ ăn nếu bằng đúng 'id' hoặc kết thúc bằng '_id', 'ma')
                if k_low == 'id' or k_low.endswith('_id') or k_low == 'ma':
                    target['id'] = str(v).strip()
                
                # Khớp Họ và tên
                elif 'ten' in k_low or 'name' in k_low or 'ho_va_ten' in k_low:
                    target['ho_va_ten'] = str(v).strip()
                    
                # Khớp Số điện thoại
                elif 'phone' in k_low or 'sdt' in k_low or 'thoai' in k_low or 'dt' in k_low:
                    target['so_dien_thoai'] = str(v).strip()
                
                # Khớp Số buổi vắng / Điểm danh
                elif 'danh' in k_low or 'vang' in k_low or 'absent' in k_low or 'attendance' in k_low or 'nghi' in k_low:
                    try:
                        target['diem_danh'] = int(v)
                    except:
                        target['diem_danh'] = 0
                
                # Khớp Dân tộc
                elif 'toc' in k_low or 'ethnic' in k_low:
                    target['dan_toc'] = str(v).strip()
                
                # Khớp Giới tính
                elif 'tinh' in k_low or 'gender' in k_low:
                    target['gioi_tinh'] = str(v).strip()
                
                # Khớp Ngày sinh
                elif 'sinh' in k_low or 'birth' in k_low:
                    target['ngay_sinh'] = str(v).strip()
                
                # Khớp Email
                elif 'email' in k_low or k_low == 'mail':
                    target['email'] = str(v).strip()
                
                # Khớp Địa chỉ (Kiểm tra chặt chẽ hơn)
                elif k_low == 'dia_chi' or k_low == 'address' or k_low == 'diachi':
                    target['dia_chi'] = str(v).strip()
                
                # Khớp Khóa học
                elif 'khoa' in k_low or 'course' in k_low:
                    target['khoa_hoc'] = str(v).strip()
                

            # Tự động đồng bộ hóa trạng thái Cảnh báo học vụ theo số buổi vắng quét được
            if target['diem_danh'] >= 5:
                target['canh_bao'] = "Cảnh báo nghỉ học"
            elif target['diem_danh'] >= 3:
                target['canh_bao'] = "Cảnh báo học tập"
            else:
                target['canh_bao'] = "Không"

            # Làm sạch object s cũ và ghi đè toàn bộ trường dữ liệu đã được chuẩn hóa vào
            s.clear()
            s.update(target)
            
        return data

    @staticmethod
    def write_file(data):
        with open(Config.NGUOI_HOC_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

class NguoiHocModel:
    @staticmethod
    def get_all():
        return DataEngine.read_file()

    @staticmethod
    def create(data):
        bat_buoc = ['ho_va_ten', 'so_dien_thoai', 'gioi_tinh', 'khoa_hoc']
        if any(not data.get(f) for f in bat_buoc):
            return False, "⚠️ Lỗi: Không được bỏ trống Họ và tên, Số điện thoại, Giới tính, Khóa học!"

        ds_nguoi_hoc = DataEngine.read_file()
        if any(nh['so_dien_thoai'] == data['so_dien_thoai'] for nh in ds_nguoi_hoc):
            return False, "❌ Từ chối: Số điện thoại này đã tồn tại trên hệ thống!"

        if not ds_nguoi_hoc:
            next_id = "001"
        else:
            max_id = max(int(nh['id']) for nh in ds_nguoi_hoc if nh['id'].isdigit())
            next_id = str(max_id + 1).zfill(3)

        new_student = {
            "id": next_id,
            "ho_va_ten": data['ho_va_ten'],
            "so_dien_thoai": data['so_dien_thoai'],
            "dan_toc": data.get('dan_toc', 'Kinh'),
            "gioi_tinh": data['gioi_tinh'],
            "ngay_sinh": data.get('ngay_sinh', '-'),
            "email": data.get('email', '-'),
            "dia_chi": data.get('dia_chi', '-'),
            "khoa_hoc": data['khoa_hoc'],
            "diem_danh": 0,
            "canh_bao": "Không"
        }
        
        ds_nguoi_hoc.append(new_student)
        DataEngine.write_file(ds_nguoi_hoc)
        return True, f"✅ Đã thêm người học thành công! Mã ID: {next_id}"

    @staticmethod
    def update(student_id, new_data):
        ds_nguoi_hoc = DataEngine.read_file()
        nh = next((s for s in ds_nguoi_hoc if s['id'] == student_id), None)
        if not nh:
            return False, "Không tìm thấy người học."

        for key in ['ho_va_ten', 'so_dien_thoai', 'gioi_tinh', 'dan_toc', 'ngay_sinh', 'email', 'dia_chi', 'khoa_hoc']:
            if key in new_data:
                nh[key] = new_data[key]

        DataEngine.write_file(ds_nguoi_hoc)
        return True, "✅ Cập nhật thông tin thành công!"

    @staticmethod
    def delete(student_id):
        ds_nguoi_hoc = DataEngine.read_file()
        filtered_data = [item for item in ds_nguoi_hoc if item['id'] != student_id]
        DataEngine.write_file(filtered_data)
        return True
