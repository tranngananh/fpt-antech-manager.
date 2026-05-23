# models.py
import json
import os
import hashlib
from config import Config


# DATA ENGINE — đọc/ghi file JSON gốc
class DataEngine:
    @staticmethod
    def initialize_db():
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        for filepath in [Config.NGUOI_HOC_FILE, Config.DIEM_DANH_FILE,
                         Config.CANH_BAO_FILE, Config.KHOA_HOC_FILE]:
            if not os.path.exists(filepath) or os.stat(filepath).st_size == 0:
                default = {} if filepath == Config.DIEM_DANH_FILE else []
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(default, f, indent=4, ensure_ascii=False)

    @staticmethod
    def read_file():
        if not os.path.exists(Config.NGUOI_HOC_FILE):
            return []
        with open(Config.NGUOI_HOC_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []

        for s in data:
            target = {
                'id':            '-',
                'ho_va_ten':     '-',
                'so_dien_thoai': '-',
                'dan_toc':       'Kinh',
                'gioi_tinh':     'Nam',
                'ngay_sinh':     '-',
                'email':         '-',
                'dia_chi':       '-',
                'khoa_hoc':      'full-stack',
                'lop_hoc':       '-',
                'so_ngay_vang':  0,
                'canh_bao':      'Không',
            }

            for k, v in s.items():
                k_low = str(k).lower().strip()

                if k_low == 'id' or k_low.endswith('_id') or k_low == 'ma':
                    target['id'] = str(v).strip()
                elif 'ten' in k_low or 'name' in k_low:
                    target['ho_va_ten'] = str(v).strip()
                elif 'thoai' in k_low or 'phone' in k_low or 'sdt' in k_low:
                    target['so_dien_thoai'] = str(v).strip()
                elif 'dan_toc' in k_low or 'ethnic' in k_low:
                    target['dan_toc'] = str(v).strip()
                elif 'gioi_tinh' in k_low or 'gender' in k_low:
                    target['gioi_tinh'] = str(v).strip()
                elif 'sinh' in k_low or 'birth' in k_low:
                    target['ngay_sinh'] = str(v).strip()
                elif 'email' in k_low or k_low == 'mail':
                    target['email'] = str(v).strip()
                elif k_low in ('dia_chi', 'address', 'diachi'):
                    target['dia_chi'] = str(v).strip()
                elif 'khoa_hoc' in k_low or 'course' in k_low:
                    target['khoa_hoc'] = str(v).strip()
                elif 'lop_hoc' in k_low or k_low == 'lop' or 'class' in k_low:
                    target['lop_hoc'] = str(v).strip()
                elif 'vang' in k_low or 'absent' in k_low:
                    try:
                        target['so_ngay_vang'] = int(v)
                    except (ValueError, TypeError):
                        target['so_ngay_vang'] = 0

            # Đồng bộ cảnh báo theo số buổi vắng
            vang = target['so_ngay_vang']
            if vang >= 5:
                target['canh_bao'] = "Cảnh báo nghỉ học"
            elif 5> vang >= 3:
                target['canh_bao'] = "Cảnh báo học tập"
            else:
                target['canh_bao'] = "Không"

            s.clear()
            s.update(target)

        return data

    @staticmethod
    def write_file(data):
        with open(Config.NGUOI_HOC_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


# ============================================================
# NGUOI HOC MODEL — nghiệp vụ học viên
# ============================================================
class NguoiHocModel:
    @staticmethod
    def get_all():
        return DataEngine.read_file()

    @staticmethod
    def get_by_id(student_id):
        data = DataEngine.read_file()
        return next((s for s in data if s['id'] == student_id), None)

    @staticmethod
    def create(data):
        bat_buoc = ['ho_va_ten', 'so_dien_thoai', 'gioi_tinh', 'khoa_hoc']
        if any(not data.get(f) for f in bat_buoc):
            return False, "⚠️ Không được bỏ trống Họ tên, SĐT, Giới tính, Khóa học!"

        ds = DataEngine.read_file()
        if any(nh['so_dien_thoai'] == data['so_dien_thoai'] for nh in ds):
            return False, "❌ Số điện thoại này đã tồn tại!"

        next_id = "001"
        if ds:
            ids = [int(nh['id']) for nh in ds if nh['id'].isdigit()]
            next_id = str(max(ids) + 1).zfill(3) if ids else "001"

        new_student = {
            "id":            next_id,
            "ho_va_ten":     data['ho_va_ten'],
            "so_dien_thoai": data['so_dien_thoai'],
            "dan_toc":       data.get('dan_toc', 'Kinh'),
            "gioi_tinh":     data['gioi_tinh'],
            "ngay_sinh":     data.get('ngay_sinh', '-'),
            "email":         data.get('email', '-'),
            "dia_chi":       data.get('dia_chi', '-'),
            "khoa_hoc":      data['khoa_hoc'],
            "lop_hoc":       data.get('lop_hoc', '-'),
            "so_ngay_vang":  0,
            "canh_bao":      "Không",
        }
        ds.append(new_student)
        DataEngine.write_file(ds)
        return True, f"✅ Đã thêm học viên thành công! Mã ID: {next_id}"

    @staticmethod
    def update(student_id, new_data):
        ds = DataEngine.read_file()
        nh = next((s for s in ds if s['id'] == student_id), None)
        if not nh:
            return False, "❌ Không tìm thấy học viên."

        for key in ['ho_va_ten', 'so_dien_thoai', 'gioi_tinh', 'dan_toc',
                    'ngay_sinh', 'email', 'dia_chi', 'khoa_hoc', 'lop_hoc']:
            if key in new_data and new_data[key]:
                nh[key] = new_data[key]

        DataEngine.write_file(ds)
        return True, "✅ Cập nhật thông tin thành công!"

    @staticmethod
    def delete(student_id):
        ds = DataEngine.read_file()
        filtered = [s for s in ds if s['id'] != student_id]
        DataEngine.write_file(filtered)
        return True, "🗑️ Đã xóa học viên khỏi hệ thống!"


# ============================================================
# DIEM DANH MODEL — bảng ngang học viên × ngày
# ============================================================
class DiemDanhModel:
    @staticmethod
    def get_all():
        if not os.path.exists(Config.DIEM_DANH_FILE):
            return {}
        with open(Config.DIEM_DANH_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    @staticmethod
    def get_ngay_list():
        data = DiemDanhModel.get_all()
        return sorted(data.keys())

    @staticmethod
    def save_all(data):
        with open(Config.DIEM_DANH_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def add_day(ngay_moi, ds_nguoi_hoc):
        """Thêm cột ngày mới — mặc định tất cả Vắng"""
        data = DiemDanhModel.get_all()
        if ngay_moi in data:
            return False, "⚠️ Ngày này đã tồn tại!"
        data[ngay_moi] = [
            {
                "id":         nh['id'],
                "ho_va_ten":  nh['ho_va_ten'],
                "lop_hoc":    nh.get('lop_hoc', '-'),
                "trang_thai": "Vắng",
            }
            for nh in ds_nguoi_hoc
        ]
        DiemDanhModel.save_all(data)
        return True, f"✅ Đã thêm ngày {ngay_moi}!"

    @staticmethod
    def delete_day(ngay):
        """Xóa cột ngày"""
        data = DiemDanhModel.get_all()
        if ngay not in data:
            return False, "❌ Ngày không tồn tại!"
        del data[ngay]
        DiemDanhModel.save_all(data)
        return True, f"🗑️ Đã xóa ngày {ngay}!"

    @staticmethod
    def sync_to_nguoi_hoc():
        """Tính lại so_ngay_vang và canh_bao cho tất cả học viên"""
        diem_danh    = DiemDanhModel.get_all()
        danh_sach_ngay = sorted(diem_danh.keys())
        ds           = DataEngine.read_file()

        for nh in ds:
            s_id   = nh['id']
            so_vang = sum(
                1 for ngay in danh_sach_ngay
                for rec in diem_danh.get(ngay, [])
                if rec['id'] == s_id and rec['trang_thai'] == 'Vắng'
            )
            nh['so_ngay_vang'] = so_vang
            if so_vang >= 5:
                nh['canh_bao'] = "Cảnh báo nghỉ học"
            elif so_vang >= 3:
                nh['canh_bao'] = "Cảnh báo học tập"
            else:
                nh['canh_bao'] = "Không"

        DataEngine.write_file(ds)


# USER MODEL — tài khoản đăng nhập
class UserModel:
    USERS_FILE = os.path.join(Config.DATA_DIR, 'users.json')

    @staticmethod
    def _hash(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def initialize(cls):
        """Tạo file users.json với admin mặc định nếu chưa có"""
        if not os.path.exists(cls.USERS_FILE) or os.stat(cls.USERS_FILE).st_size == 0:
            default = [
                {
                    "username":      "admin",
                    "password":      cls._hash("admin123"),
                    "role":          "admin",
                    "ho_ten":        "Quản trị viên",
                    "email":         "",  # ← thêm
                    "so_dien_thoai": "",  # ← thêm
                    "dia_chi":       "",  # ← thêm
                }
            ]
            with open(cls.USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(default, f, indent=4, ensure_ascii=False)

    @classmethod
    def _read(cls):
        cls.initialize()
        with open(cls.USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def _save(cls, users):
        with open(cls.USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    @classmethod
    def get_all(cls):
        return cls._read()

    @classmethod
    def authenticate(cls, username, password):
        users  = cls._read()
        hashed = cls._hash(password)
        return next(
            (u for u in users if u['username'] == username and u['password'] == hashed),
            None
        )

    @classmethod
    def create(cls, username, password, role='staff', ho_ten='',
               email='', so_dien_thoai='', dia_chi=''):          # ← thêm
        if not username or not password:
            return False, "⚠️ Không được để trống tên đăng nhập và mật khẩu!"
        users = cls._read()
        if any(u['username'] == username for u in users):
            return False, "❌ Tên đăng nhập đã tồn tại!"
        users.append({
            "username":      username,
            "password":      cls._hash(password),
            "role":          role,
            "ho_ten":        ho_ten,
            "email":         email,         # ← thêm
            "so_dien_thoai": so_dien_thoai, # ← thêm
            "dia_chi":       dia_chi,       # ← thêm
        })
        cls._save(users)
        return True, f"✅ Đã tạo tài khoản {username} ({role})!"

    @classmethod
    def change_password(cls, username, old_password, new_password):
        users = cls._read()
        user  = next((u for u in users if u['username'] == username), None)
        if not user:
            return False, "❌ Không tìm thấy tài khoản!"
        if user['password'] != cls._hash(old_password):
            return False, "❌ Mật khẩu cũ không đúng!"
        if not new_password:
            return False, "⚠️ Mật khẩu mới không được để trống!"
        user['password'] = cls._hash(new_password)
        cls._save(users)
        return True, "✅ Đổi mật khẩu thành công!"

    @classmethod
    def delete(cls, username):
        users    = cls._read()
        filtered = [u for u in users if u['username'] != username]
        if len(filtered) == len(users):
            return False, "❌ Không tìm thấy tài khoản!"
        # Không cho xóa hết admin
        if not any(u['role'] == 'admin' for u in filtered):
            return False, "❌ Phải giữ lại ít nhất 1 tài khoản admin!"
        cls._save(filtered)
        return True, f"✅ Đã xóa tài khoản {username}!"